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

#line = re.sub('[!@#$]', '', line)

def connectMongoDB(dbname,colname):
	#connect to mongodb
	client = MongoClient('localhost', 27017)
	# Get the database
	db = client[dbname]
	collection = db[colname]
	return collection
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def	MongotoPTMannotation(proteinIDs,Tag_FTs,output_types,output_prefix):
	pass

def tableGeneration(filepath,fts):
	# Open a file
	id_flag = 0
	out_position = []
	out_data = dict()
	with open(filepath) as fp:
		for line in fp:
			collapsed = ' '.join(line.split())
			data = collapsed.split(";")
			parsed_1 = data[0].split(" ")
			if parsed_1[0] == "ID" and  id_flag == 0:
				id_flag = 1
				out_id = parsed_1[1]	
			##[go,interpro,pfam,prosite,smart,supfam]
			elif parsed_1[0] == "FT":
				if len(parsed_1) > 4:
					ft = ''
					for i in range(4,len(parsed_1)):
						ft = ft +  parsed_1[i]
					ft = re.sub('[.]', '', ft)
					
					if ft in fts:
						print('yes')
						out_position.append(parsed_1[2])
						out_position.append(parsed_1[3])
						out_position = remove_duplicates(out_position)
						fts.setdefault(ft, []).append(out_position)
						out_position = []
			##
			elif parsed_1[0] == '//':
				print(fts)
				fts = {'Phosphoserine' : [],'Phosphothreonine' : [],'N6-acetyllysine' : [],'Omega-N-methylarginine' : []
				,'N6-methyllysine' : [],'N6,N6-dimethyllysine' : [], 'N6,N6,N6-trimethyllysine' : [],'N-linked(GlcNAc)asparagine' : []
				,'S-palmitoylcysteine': [],'Pyrrolidonecarboxylicacid':[]}
				##rewind
				id_flag = 0	
				out_position = []
	fp.close()

def main():
	# parser = argparse.ArgumentParser()
	# parser.add_argument('-l', help="local filepath", required=True)
	# args = parser.parse_args()
	fts = {'Phosphoserine' : [],'Phosphothreonine' : [],'N6-acetyllysine' : [],'Omega-N-methylarginine' : []
	,'N6-methyllysine' : [],'N6,N6-dimethyllysine' : [], 'N6,N6,N6-trimethyllysine' : [],'N-linked(GlcNAc)asparagine' : []
	,'S-palmitoylcysteine': [],'Pyrrolidonecarboxylicacid':[]}
	tableGeneration('test2.txt',fts)
	# filepath = args.l
	
	# if os.path.exists(filepath):
		# tableGeneration(filepath,fts):
			
	# else:
		# print("File does not exist\n")
		# sys.exit()
  
if __name__== "__main__":
	main()



