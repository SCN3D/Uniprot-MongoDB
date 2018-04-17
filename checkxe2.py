import sys
import os.path
import argparse
import re
import itertools

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', help="python script to check", required=True)
	args = parser.parse_args()
	with open(parser.l) as fp:
		for i, line in enumerate(fp):
			if "\xe2" in line:
				print (i)	
if __name__== "__main__":
	main()