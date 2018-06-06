import functions
import json

def main():

	dbname = 'uniprot'
	colname = 'table'

	collection = functions.connectMongoDB(dbname,colname)
	results = collection.find({})
	display = {'Phosphoserine':0,'Phosphothreonine':0,'Phosphotyrosine':0,'N6-acetyllysine':0,'Omega-N-methylarginine':0,
				'N6-methyllysine':0,'N6,N6-dimethyllysine':0,'N6,N6,N6-trimethyllysine':0,'N-linked(GlcNAc)asparagine':0,
				'S-palmitoylcysteine': 0,'Pyrrolidonecarboxylicacid':0,'Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)':0
				}
	for data in results:
		for ptm in display:
			if ptm in data:
				display[ptm] += len(data[ptm])
	print(display)
	with open('display.txt', 'w') as outfile:
		json.dump(display, outfile)



if __name__== "__main__":
	main()
