#
#!/usr/bin/python
#vm: amazon linux 2 AMI
#python 2.7.5
#mongodb 3.6.3
import pymongo
from pymongo import MongoClient
import sys
import os.path
import argparse
import re
import itertools
import functions
	
#insert # after ptm position in seq, format: fasta
def duolin(id,ft,seq):
	seq_list = list(seq)
	for i in ft:
		seq_list.insert(int(i),'#')
	
	sequence = ''.join(seq_list)
	out_data = '>'+id+'\n'+sequence
	return out_data
	
#if there is ft add 1 after id, format: fasta
def chunhui(id,seq):
	out_data = '>'+id+' 1\n'+seq
	return out_data


#output_type 1: duolin 0:chunhui 
def	MongotoPTMannotation(proteinIDs,Tag_FTs,output_types,output_prefix):
	table = functions.connectMongoDB('test','table')
	entry = functions.connectMongoDB('uniprot','entry')
	file = []
	out_data = ''
	
	if not os.path.exists(output_prefix):
		os.makedirs(output_prefix)
	
	for index, tag in enumerate(Tag_FTs):
		file.append(open(output_prefix+'/'+tag+'.fasta','w'))
		
	
	for id in proteinIDs:
		ptm = table.find_one({'_id': id})
		ft_index = []
		print(ptm)
		for index, ft in enumerate(Tag_FTs):
			# ft = re.sub('[.]', '',ft) #take off .
			unfold_ft = ft.split(" ")
			
			for new_ft in unfold_ft:
				if new_ft in ptm:
					ft_index.extend(ptm[new_ft]) 
					
			if len(ft_index) >= 1:
				sequence = ptm['sequence']
				if output_types == 1: #DUOLIN
					out_data = duolin(ptm['_id'],ft_index,sequence)
				else: #CHUNHUI	
					out_data = chunhui(ptm['_id'],sequence)
				file[index].write(out_data)
					
	for index, tag in enumerate(Tag_FTs):
		file[index].close()
		
#requirement: 1. uniprotCreateDB.py   2. tableGeneration.py 
#example annotaion.py -l 'uniprot '
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-fts', nargs='+', help="feature keys", required=True)
	parser.add_argument('-ids', nargs='+', help="id list", required=True)
	parser.add_argument('-type', type=int, choices=[0,1], help="type 1 for duolin, type 0 for chunhui", required=True)
	parser.add_argument('-out', help="output folder name", required=True)
	args = parser.parse_args()
	# fts = ['Phosphoserine','N6-methyllysine','Phosphothreonine','Phosphotyrosine',
	# 'N6-acetyllysine','Omega-N-methylarginine','N6,N6-dimethyllysine','N6,N6,N6-trimethyllysine','N-linked(GlcNAc)asparagine',
	# 'S-palmitoylcysteine','Pyrrolidonecarboxylicacid','Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)']
	ids = args.ids
	fts = args.fts
	type = args.type
	
	# print(fts)
	
	folder_path = args.out
	
	MongotoPTMannotation(ids,fts,1,folder_path)
  
if __name__== "__main__":
	main()



