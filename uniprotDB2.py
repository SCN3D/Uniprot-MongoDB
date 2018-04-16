#!/usr/bin/python
#vm: amazon linux 2 AMI
#python 2.7.5
#mongodb 3.6.3
import pymongo
from pymongo import MongoClient
import sys
import os.path
import argparse
from crontab import CronTab
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create a file handler
handler = logging.FileHandler('DBoperations.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

#*.py -l filepath -db dbname -col collection_name -f [go,interpro,pfam,prosite,smart,supfam] or all -update (months)
 
def connectMongoDB(dbname,colname):
	#connect to mongodb
	client = MongoClient('localhost', 27017)
	# Get the database
	db = client[dbname]
	collection = db[colname]
	return collection
	
def updateMongoDB(filepath,features,collection):
	# Open a file
	id_flag = 0
	ac_flag = 0
	out_ac = []
	sequence = ''

	out_data = dict()
	with open(filepath) as fp:
		for line in fp:
			collapsed = ' '.join(line.split())
			data = collapsed.split(";")
			parsed_1 = data[0].split(" ")
			if parsed_1[0] == "ID" and  id_flag == 0:
				id_flag = 1
				out_id = parsed_1[1]
				
			elif parsed_1[0] == "AC" and  ac_flag == 0:
				ac_flag = 1	
				out_ac.append(parsed_1[1])
				if len(data)  > 2:
					for x in range(1, len(data)-1):
						out_ac.append(data[x])
				out_data = {'_id' : out_id,'ac':out_ac}
			elif len(parsed_1[0]) > 2:
				sequence += collapsed
			##[go,interpro,pfam,prosite,smart,supfam]
			elif parsed_1[0] == "DR" and  parsed_1[1].lower() in features:
				if features[parsed_1[1].lower()] == 1:
					parsed_2 = data[1].split(" ")
					if parsed_1[1].lower() in out_data:
						out_data[parsed_1[1].lower()].append(parsed_2[1])
					else:
						out_data[parsed_1[1].lower()] = [parsed_2[1]]
			##
			elif parsed_1[0] == '//':
				sequence = ''.join(sequence.split())
				out_data['sequence'] = sequence
				collection.save(out_data)
				##rewind
				id_flag = 0
				ac_flag = 0
				out_ac = []
				sequence = ''
			
			
	fp.close()
		
def createCrontab(dbname, colname, features, update):
	my_cron = CronTab(user='ec2-user')
	fs = ' '.join(features)
	cmd = "/usr/bin/python /home/ec2-user/test/uniprotDB.py -l /home/ec2-user/test/test2.txt -db %s -col %s -f %s" % (dbname, colname, fs)
	job = my_cron.new(command=cmd)
	job.month.every(update)
	my_cron.write()
	for job in my_cron:
		print (job)
		
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', help="local filepath", required=True)
	parser.add_argument('-db', help="database name", required=True)
	parser.add_argument('-col', help="collection name", required=True)
	parser.add_argument('-f', nargs='+', help="features [go,interpro,pfam,prosite,smart,supfam]", required=True)
	parser.add_argument('-update', type=int, default=0, help="update options [#](every # months) , default to manual(0)")
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
				
		collection = connectMongoDB(dbname,colname)
		logger.info('Update Data Base')
		updateMongoDB(filepath,features,collection)
		
		if args.update > 0:
			createCrontab(dbname, colname, args.f,args.update)
			logger.info("set auto update every {0} month".format(args.update))
			#print("set auto update every {0} month".format(args.update))
			
		logger.info('Finish!')
			
	else:
		logger.warn('File does not exist')
		sys.exit()
	
  
if __name__== "__main__":
	main()


