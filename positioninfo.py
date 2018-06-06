import functions
import json
from acs import pos_total
def main():
    dbname = 'uniprot'
    colname = 'table'
    collection = functions.connectMongoDB(dbname,colname)
    acs = ['Q6GZW8']
    write2file = []
    ##
    with open('positionInfo.txt', 'w') as outfile:
        for ac in acs:
            result = collection.find_one({'ac':ac})
            print(ac)
            if 'Glycyllysineisopeptide(Lys-Gly)(interchainwithG-Cterinubiquitin)' in result:
                print(result['Glycyllysineisopeptide(Lys-Gly)(interchainwithG-Cterinubiquitin)'])
                temp = {'AC': ac,'Positions':result['Glycyllysineisopeptide(Lys-Gly)(interchainwithG-Cterinubiquitin)']}
                write2file.append(temp)
            else:
                print('None!')
        json.dump(write2file, outfile)
if __name__== "__main__":
    main()
