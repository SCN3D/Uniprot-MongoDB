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
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def	MongotoPTMannotation(proteinIDs,Tag_FTs,output_types,output_prefix):
	pass

def tableGeneration(filepath,fts):
	table = connectMongoDB('test','table')
	# Open a file
	id_flag = 0
	out_position = []
	out_data = dict()
	special = 0
	with open(filepath) as fp:
		for line in fp:
			collapsed = ' '.join(line.split())
			data = collapsed.split(";")
			parsed_1 = data[0].split(" ")
			if parsed_1[0] == "ID" and  id_flag == 0:
				id_flag = 1
				out_id = parsed_1[1]
				out_data = {'_id' : out_id}
			##[go,interpro,pfam,prosite,smart,supfam]
			elif parsed_1[0] == "FT":
				if len(parsed_1) > 4 and special == 0:
					ft = ''
					for i in range(4,len(parsed_1)):
						ft = ft + parsed_1[i]
					ft = re.sub('[.]', '', ft)
					out_position = remove_duplicates([parsed_1[2],parsed_1[3]])
					if ft == 'Glycyllysineisopeptide(Lys-Gly)':
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
			##
			elif parsed_1[0] == '//':
				fts = dict( [(k,list(itertools.chain.from_iterable(v))) for k,v in fts.items() if len(v)>0]) #delete empty FTs from dictionary ##list(itertools.chain.from_iterable(v)) format 
				out_data = merge_two_dicts(out_data,fts)
				print(out_data)
				table.save(out_data)
				fts = {'Phosphoserine':[],'Phosphothreonine':[],'Phosphotyrosine':[],'N6-acetyllysine':[],'Omega-N-methylarginine':[],
				'N6-methyllysine':[],'N6,N6-dimethyllysine':[],'N6,N6,N6-trimethyllysine':[],'N-linked(GlcNAc)asparagine':[],
				'S-palmitoylcysteine': [],'Pyrrolidonecarboxylicacid':[],'Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)':[]}
				
				##rewind
				id_flag = 0	
				out_position = []
	fp.close()

def main():
	# parser = argparse.ArgumentParser()
	# parser.add_argument('-l', help="local filepath", required=True)
	# args = parser.parse_args()
	fts = {'Phosphoserine':[],'Phosphothreonine':[],'Phosphotyrosine':[],'N6-acetyllysine':[],'Omega-N-methylarginine':[],
	'N6-methyllysine':[],'N6,N6-dimethyllysine':[],'N6,N6,N6-trimethyllysine':[],'N-linked(GlcNAc)asparagine':[],
	'S-palmitoylcysteine': [],'Pyrrolidonecarboxylicacid':[],'Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)':[]}
	tableGeneration('test2.txt',fts)
	# filepath = args.l
	
	# if os.path.exists(filepath):
		# tableGeneration(filepath,fts):
			
	# else:
		# print("File does not exist\n")
		# sys.exit()
  
if __name__== "__main__":
	main()



