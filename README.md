# Uniprot-MongoDB
MongoDB with uniprot
usage: uniprotDB.py [-h] -l L -db DB -col COL -f F [F ...] [-update [UPDATE]]

optional arguments:
  -h, --help        show this help message and exit
  -l L              local filepath
  -db DB            database name
  -col COL          collection name
  -f F [F ...]      features [go,interpro,pfam,prosite,smart,supfam]
  -update [UPDATE]  update option[1,2,3,4,5……], default to manual(0)
