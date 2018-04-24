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

def connectMongoDB(dbname,colname):
	#connect to mongodb
	client = MongoClient('localhost', 27017)
	# Get the database
	db = client[dbname]
	collection = db[colname]
	return collection
	
#insert # after ptm position in seq
def duolin(id,ft,seq):
	seq_list = list(seq)
	for i in ft:
		seq_list.insert(int(i),'#')
	
	sequence = ''.join(seq_list)
	out_data = '>'+id+'\n'+sequence
	return out_data
	
#if there is ft add 1 after id
def chunhui(id,seq):
	out_data = '>'+id+' 1\n'+seq
	return out_data


#output_type 1: duolin 2:chunhui 
def	MongotoPTMannotation(proteinIDs,Tag_FTs,output_types,output_prefix):
	table = connectMongoDB('test','table')
	entry = connectMongoDB('uniprot','entry')
	file = []
	out_data = ''
	
	if not os.path.exists(output_prefix):
		os.makedirs(output_prefix)
	
	for index, tag in enumerate(Tag_FTs):
		file.append(open(output_prefix+'/'+tag+'.fasta','w'))
		
	if output_types == 1: #DUOLIN
		for id in proteinIDs:
			ptm = table.find_one({'_id': id})
			print(ptm)
			for index, ft in enumerate(Tag_FTs):
				ft = re.sub('[.]', '',ft) #take off .
				if ft in ptm:
					seq = entry.find_one({'_id': id},{'sequence': 1})
					sequence = seq['sequence']
					out_data = duolin(ptm['_id'],ptm[ft],sequence)
					print(ft)
					print(out_data)
					file[index].write(out_data)
					
	else: #CHUNHUI
		for id in proteinIDs:
			ptm = table.find_one({'_id': id})
			print(ptm)
			for index, ft in enumerate(Tag_FTs):
				ft = re.sub('[.]', '',ft)
				if ft in ptm:
					seq = entry.find_one({'_id': id},{'sequence': 1})
					sequence = seq['sequence']
					out_data = chunhui(ptm['_id'],sequence)
					print(ft)
					print(out_data)
					file[index].write(out_data)
					
	for index, tag in enumerate(Tag_FTs):
		file[index].close()

def main():
	# parser = argparse.ArgumentParser()
	# parser.add_argument('-l', help="local filepath", required=True)
	# parser.add_argument('-ft', nargs='+', help="feature keys", required=True)
	# parser.add_argument('-id', nargs='+', help="id list", required=True)
	# args = parser.parse_args()
	fts = ['Phosphoserine','N6-methyllysine','Phosphothreonine','Phosphotyrosine',
	'N6-acetyllysine','Omega-N-methylarginine','N6,N6-dimethyllysine','N6,N6,N6-trimethyllysine','N-linked(GlcNAc)asparagine',
	'S-palmitoylcysteine','Pyrrolidonecarboxylicacid','Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)']
	ids = ['001R_FRG3G','002L_FRG3G','003L_IIV3','003R_FRG3G','004R_FRG3G','005L_IIV3','005R_FRG3G','006L_IIV6','006R_FRG3G']
	
	MongotoPTMannotation(ids,fts,1,'test')
	# filepath = args.l
	
	# if os.path.exists(filepath):
		#fts = args.ft
		#ids = args.id
		# tableGeneration(filepath,fts):
			
	# else:
		# print("File does not exist\n")
		# sys.exit()
  
if __name__== "__main__":
	main()



