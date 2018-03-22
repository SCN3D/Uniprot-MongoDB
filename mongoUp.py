#!/usr/bin/python
import pymongo
from pymongo import MongoClient
import sys
import os.path
import csv


#*.py -l filepath -db dbname -col collection_name -id primarykey_name -f [.....] or all

# count the arguments
arguments = len(sys.argv) - 1  
filepath = ''
dbname = ''
colname = ''
dictionary = dict()
all = 0
pk = ''
if arguments > 9 and sys.argv[1] == "-l" and sys.argv[3] == "-db" and sys.argv[5] == "-col" and sys.argv[7] == "-id" and sys.argv[9] == "-f":
	if os.path.exists(sys.argv[2]):
		# file exists
		filepath = sys.argv[2]
	else:
		print("File does not exist\n")
		sys.exit()
	dbname = sys.argv[4]
	colname = sys.argv[6]
	pk = sys.argv[8].lower()
	dictionary[pk] = 1
	if sys.argv[10] == 'all':
		all = 1
	else:
		for i in range(10,arguments):
			dictionary[sys.argv[i].lower()] = 1
else:
	print("Syntax:\n*.py -l filepath -db dbname -col collection_name -id primarykey_name -f [.....] or all\n")
	sys.exit()

#connect to mongodb
client = MongoClient('localhost', 27017)
# Get the database
db = client[dbname]
collections = db[colname]
out_data = dict()
with open(filepath) as f:
	csv_f = csv.reader(f)
	for i, row in enumerate(csv_f):
		print(i)
		if i == 0:
			if all == 1:
				for j, field in enumerate(row):
					dictionary[field.lower()] = j  
			else:
				for j, field in enumerate(row):
					if field.lower() in dictionary:
						dictionary[field.lower()] = j 
		else:
			out_data = {'_id' : row[dictionary[pk]]}
			for field in dictionary:
				if field != pk:
					out_data[field] = row[dictionary[field]]
			collections.save(out_data)
f.close()
print("done!")