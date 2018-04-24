import feedparser
from datetime import datetime as dt
import urllib
import gzip
import shutil
import pymongo
from pymongo import MongoClient
import sys
import os.path
import argparse
from crontab import CronTab
import configparser

def rssread():
	url = 'https://www.uniprot.org/news/?format=rss'

	feed = feedparser.parse(url )

	date = feed['updated'].split(' ')
	new_date = date[1]+'/'+date[2]+'/'+date[3]

	new_date = dt.strptime(new_date,"%d/%b/%Y")
	return new_date

def getUniprot():
	uniprot_url = 'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz'
	urllib.urlretrieve(file_url, 'uniprot.txt.gz')
	print("Unzip file...")
	with gzip.open('uniprot.txt.gz', 'rb') as f_in:
		with open('uniprot.txt', 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)
	print("File name:uniprot.txt")


def valid_date(s):
    try:
        return datetime.strptime(s, "%d/%m/%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def connectMongoDB(dbname,colname):
	#connect to mongodb
	client = MongoClient('localhost', 27017)
	# Get the database
	db = client[dbname]
	collection = db[colname]
	return collection
def updateMongoDB(filepath,features,collection,date):
	train = 1 
	if date == "0/0/0":
		train = 0
	try:
		old_date = datetime.strptime(date, "%d/%m/%Y")
	except ValueError:
		print("Invalid date!")
		sys.exit()
		
	# Open a file
	out_date = datetime.strptime("0/0/0", "%d/%m/%Y")
	id_flag = 0
	ac_flag = 0
	out_ac = []
	sequence = ''
	out_data = dict()
	train_ids = []
	

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
			elif parsed_1[0] == "DT":
				temp_date = datetime.strptime(parsed_1[1], "%d-%b-%Y")
				if temp_date > out_date:
					out_date = temp_date
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
				out_data['date'] = out_date
				collection.save(out_data)
				
				if train == 1 and old_date <= out_date:
					train_ids.append(out_id)
					
				##rewind
				id_flag = 0
				ac_flag = 0
				out_ac = []
				sequence = ''
				out_date = datetime.strptime("0/0/0", "%d/%m/%Y")
	fp.close()
	if train == 1:
		ids_file = open(“train_ids.txt”,”w”)
		for id in train_ids:
			ids_file.write(id)
		ids_file.close()

#a crontab job scheduler		
def setAutoUpdate(dbname, colname, features, train, update):
	my_cron = CronTab(user='ec2-user')
	fs = ' '.join(features)
	cmd = "/usr/bin/python /home/ec2-user/Uniprot-MongoDB/rssReader.py -db "+dbname+" -col "+colname+" -f "+fs+" -train "+train
	job = my_cron.new(command=cmd)
	job.month.every(update)
	my_cron.write()
	for job in my_cron:
		print (job)
		
def Config_edit(date):
	config = configparser.ConfigParser()
	config['DEFAULT'] = {'date': date}
	with open('config.ini', 'w') as configfile:
		config.write(configfile)