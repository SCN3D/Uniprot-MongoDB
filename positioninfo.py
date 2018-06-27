import functions
import json
from acs import pos_total as acs
def main():
    dbname = 'uniprot'
    colname = 'ubiquitinTable'
    collection = functions.connectMongoDB(dbname,colname)
    write2file = []
    takeoff = ['_id','ac']
    ##
    with open('positionInfo.txt', 'w') as outfile:
        for ac in acs:
            result = collection.find_one({'ac':ac})
            print(ac)
            temp = {'AC': ac}
            for output in result:
                if output not in takeoff:
                    temp[output] = result[output]
            write2file.append(temp)
        json.dump(write2file, outfile)
if __name__== "__main__":
    main()
