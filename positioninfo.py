import functions
import json
from acs import pos_total as acs
def main():
    dbname = 'uniprot'
    colname = 'ubiquitinTable'
    collection = functions.connectMongoDB(dbname,colname)
    write2file = []
    ##
    with open('positionInfo.txt', 'w') as outfile:
        for ac in acs:
            result = collection.find_one({'ac':ac})
            print(ac)
            temp = {'AC': ac}
            for output in result:
                print(result[output])
                temp[output] = {output:result[output]}
            write2file.append(temp)
        json.dump(write2file, outfile)
if __name__== "__main__":
    main()
