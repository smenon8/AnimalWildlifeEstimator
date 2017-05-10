'''
Author: Sreejith Menon (smenon8@uic.edu)
Date: May 10, 2017

	* Script for setting up mongodb instance with all the files
	* Below is the list of required files (will be updated as and when new files are added)

List of files required (generally stored under ../data/)
'''

from pymongo import MongoClient
import json

# added for future
params = {
	'db_name' : 'AWESOME_DS',
}

def get_mongod_db(conn_cfg=params):
	client = MongoClient()
	return client[conn_cfg.get('db_name')]

'''
Expects MongoD database object and table name tbl_nm as a string
'''
def get_mongodb_tab(db_obj, tbl_nm):
	return db_obj.get_collection(tbl_nm)


'''
Creates works only when the table tbl_nm does not exist
Once created, it adds the document specified by doc(JSON expected) to the table
'''
def create_table(db_obj, doc, tbl_nm):
	tbl = db_obj[tbl_nm]

	try:
		for key in doc.keys():
			tbl.insert(doc.get(key))
	except Exception as e:
		print("Insert failure..!")
		return e

	return 0

'''
Expects MongoD table object and a query in dict/BSON format
Returns a cursor which is an iterable
'''
def query_tab(tbl_obj, query):
	
	return tbl_obj.find(query)

