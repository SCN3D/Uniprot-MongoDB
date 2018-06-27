#id_ft table
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


def ubiquitin(filepath,fts):
	table = functions.connectMongoDB('uniprot','ubiquitinTable')
	# Open a file
	ac_flag = 0
	out_ac = []
	out_position = []
	out_data = dict()
	special = 0
	specials = ['Glycyllysineisopeptide(Lys-Gly)','Peptide(Met-Gly)(interchainwithG-Cter','Glycylserineester(Ser-Gly)','Glycylcysteinethioester(Cys-Gly)']
	with open(filepath) as fp:
		for line in fp:
			collapsed = ' '.join(line.split())
			data = collapsed.split(";")
			parsed_1 = data[0].split(" ")
			if parsed_1[0] == "AC" and  ac_flag == 0:
				ac_flag = 1	
				out_ac.append(parsed_1[1])
				if len(data)  > 2:
					for x in range(1, len(data)-1):
						out_ac.append(data[x])
				out_data = {'ac':out_ac}
			##[go,interpro,pfam,prosite,smart,supfam]
			elif parsed_1[0] == "FT":
				if len(parsed_1) > 4 and special == 0:
					ft = ''
					for i in range(4,len(parsed_1)):
						ft = ft + parsed_1[i]
					ft = re.sub('[.]', '', ft)
					out_position = functions.remove_duplicates([parsed_1[2],parsed_1[3]])
					if ft in specials:
						special = 1
						continue
					if ft in fts:
						fts.setdefault(ft, []).append(out_position)
						out_position = []
				elif special == 1:
					for i in range(1,len(parsed_1)):
						ft = ft + parsed_1[i]
					ft = re.sub('[.]', '', ft)
					if ft in fts:
						fts.setdefault(ft, []).append(out_position)
						out_position = []
					special = 0
			elif parsed_1[0] == '//':
				fts = dict( [(k,list(itertools.chain.from_iterable(v))) for k,v in fts.items() if len(v)>0]) #delete empty FTs from dictionary ##list(itertools.chain.from_iterable(v)) format 
				out_data = functions.merge_two_dicts(out_data,fts)
				#print(out_data)
				table.save(out_data)
				fts = {'Glycyllysineisopeptide(Lys-Gly)(interchainwithG-Cterinubiquitin)':[],'Glycylserineester(Ser-Gly)(interchainwithG-Cterinubiquitin)':[],
                'Peptide(Met-Gly)(interchainwithG-Cterinubiquitin)':[],'Glycylcysteinethioester(Cys-Gly)(interchainwithG-Cterinubiquitin)':[]}
				
				##rewind
				out_ac = []
				ac_flag = 0
				out_position = []
				
	fp.close()
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', default='uniprot.txt',help="local filepath")
	args = parser.parse_args()
	filepath = args.l
	
	
	
	fts = fts = {'Glycyllysineisopeptide(Lys-Gly)(interchainwithG-Cterinubiquitin)':[],'Glycylserineester(Ser-Gly)(interchainwithG-Cterinubiquitin)':[],
    'Peptide(Met-Gly)(interchainwithG-Cterinubiquitin)':[],'Glycylcysteinethioester(Cys-Gly)(interchainwithG-Cterinubiquitin)':[]}
	
	filepath = args.l
	
	if os.path.exists(filepath):
		ubiquitin(filepath,fts)
			
	else:
		print("File does not exist\n")
		sys.exit()
  
if __name__== "__main__":
	main()



