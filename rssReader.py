#!/usr/bin/python
#vm: amazon linux 2 AMI
#python 2.7.5
#mongodb 3.6.3
import functions.py
import argparse
import sys

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-db', help="database name", required=True)
	parser.add_argument('-col', help="collection name", required=True)
	parser.add_argument('-f', nargs='+', help="features [go,interpro,pfam,prosite,smart,supfam]", required=True)
	parser.add_argument('-train', type=int, default=0, help="for auto train set 1 to auto train")
	
	args = parser.parse_args()
	
	features = {
		'go' : 0,'interpro' : 0,'pfam' : 0,'prosite' : 0,'smart' : 0,'supfam' : 0
	}
	dbname = args.db
	colname = args.col
	train = args.train
	collection = functions.connectMongoDB(dbname,colname)
	
	if len(args.f) == 1 and args.f[0].lower() == 'all':
			features = {'go' : 1,'interpro' : 1,'pfam' : 1,'prosite' : 1,'smart' : 1,'supfam' : 1}
	else:
		for i in args.f:
			features[i.lower()] = 1
			
	config = configparser.ConfigParser()
	config.read('config.ini')
	old_date = config['DEFAULT']['date']
	new_date = rssread()
	
	if new_date > old_date:
		getUniprot()
		if train == 0:
			functions.updateMongoDB('uniprot.txt',features,collection,"1/1/1111")
			functions.Config_edit(new_date)
		elif train == 1:
			functions.updateMongoDB('uniprot.txt',features,collection,new_date)
			functions.Config_edit(new_date)
		else:
			print("error")
if __name__== "__main__":
	main()
