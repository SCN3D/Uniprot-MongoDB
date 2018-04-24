#!/usr/bin/python
#vm: amazon linux 2 AMI
#python 2.7.5
#mongodb 3.6.3
import functions
import sys
import os.path
import argparse
import datetime as dt

# usage: uniprotDB.py [-h] -l L -db DB -col COL -f F [F ...] [-update [UPDATE]]
#
# optional arguments:
#  -h, --help        show this help message and exit
#  -l L              local filepath
#  -db DB            database name
#  -col COL          collection name
#  -f F [F ...]      features [go,interpro,pfam,prosite,smart,supfam]
#  -update [UPDATE]  update option[1,2,3,4,5], default to manual 0

		
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', help="local filepath", required=True)
	parser.add_argument('-db', help="database name", required=True)
	parser.add_argument('-col', help="collection name", required=True)
	parser.add_argument('-f', nargs='+', help="features [go,interpro,pfam,prosite,smart,supfam]", required=True)
	parser.add_argument('-update', type=int, default=0, help="update options [#](every # months) , default to manual(0)")
	parser.add_argument('-train', type=int, choices=[0,1],default=0, help="set 1 to auto train")

	args = parser.parse_args()
	
	filepath = args.l
	features = {
		'go' : 0,'interpro' : 0,'pfam' : 0,'prosite' : 0,'smart' : 0,'supfam' : 0
	}
	dbname = args.db
	colname = args.col
	
	if os.path.exists(filepath):
		if len(args.f) == 1 and args.f[0].lower() == 'all':
			features = {'go' : 1,'interpro' : 1,'pfam' : 1,'prosite' : 1,'smart' : 1,'supfam' : 1}
		else:
			for i in args.f:
				features[i.lower()] = 1
				
		collection = functions.connectMongoDB(dbname,colname)
		functions.updateMongoDB(filepath,features,collection,"0/0/0")
		functions.Config_edit(dt.now())
		
		if args.update > 0:
			functions.setAutoUpdate(dbname, colname, args.f, args.train, args.update)
			print("Check for update every "+args.update+" months!")
	else:
		print("File does not exist\n")
		sys.exit()
	
  
if __name__== "__main__":
	main()



