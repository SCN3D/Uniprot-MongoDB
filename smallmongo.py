#!/usr/bin/python
import pymongo
from pymongo import MongoClient
import sys
import os.path
import csv
import argparse

#*.py -l filepath -db dbname -col collection_name -id primarykey_name -f [.....] or all
#input format: csv, delimiter: ','
# 0: a,b,c,d (feature names)
# 1: 1,2,3,4
# 2: 5,6,7,8
def connectMongoDB(dbname,colname):
	#connect to mongodb
	client = MongoClient('localhost', 27017)
	# Get the database
	db = client[dbname]
	collection = db[colname]
	return collection
	
def updateMongoDB(filepath,dictionary,collection,primaryKey,featureFlag):
	collections = collection
	out_data = dict()
	with open(filepath) as f:
		csv_f = csv.reader(f)
		for i, row in enumerate(csv_f):
			print(i)
			if i == 0:
				if featureFlag == 1:
					for j, field in enumerate(row):
						dictionary[field.lower()] = j  
				else:
					for j, field in enumerate(row):
						if field.lower() in dictionary:
							dictionary[field.lower()] = j 
			else:
				out_data = {'_id' : row[dictionary[primaryKey]]}
				for field in dictionary:
					if field != primaryKey:
						out_data[field] = row[dictionary[field]]
				collections.save(out_data)
	f.close()
	print("done!")
	
def main():
	dictionary = dict()
	all = 0

	parser = argparse.ArgumentParser()
	parser.add_argument('-l', help="local filepath", required=True)
	parser.add_argument('-db', help="database name", required=True)
	parser.add_argument('-col', help="collection name", required=True)
	parser.add_argument('-id', help="primary key name", required=True)
	parser.add_argument('-f', nargs='+', default="all", help="features name [...] or all", required=True)
	args = parser.parse_args()
	
	filepath = args.l
	
	
	if os.path.exists(filepath):
		# file exists
		dbname = args.db
		colname = args.col
		pk = args.id.lower()
		dictionary[pk] = 1
		if args.f[0].lower() == 'all':
			all = 1
		else:
			for i in args.f:
				dictionary[i.lower()] = 1
				
		collection = connectMongoDB(dbname,colname)
		updateMongoDB(filepath,dictionary,collection,pk,all)
	else:
		print("File does not exist\n")
		sys.exit()
	
  
if __name__== "__main__":
	main()