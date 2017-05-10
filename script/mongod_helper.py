'''
Author: Sreejith Menon (smenon8@uic.edu)
Date: May 10, 2017

	* Methods to interface with an instance of mongod database
	* Can be modified to connect to any mongod instance and perform basic operations
	* Methods to drop table, modify database etc. planned to be written in the future.
'''

from pymongo import MongoClient, errors

# added for future
params = {
	'db_name' : 'AWESOME_DS',
	'maxSevSelDelay' : 1
}

def check_mongod_running(conn_cfg=params):
	client = MongoClient(serverSelectionTimeoutMS=conn_cfg.get('maxSevSelDelay', 1))
	try:
		client.server_info()
	except errors.ServerSelectionTimeoutError as err:
		print("MongoDB instance has not started or is dead..!")
		client = err

	return client

def get_mongod_db(conn_cfg=params):
	client = check_mongod_running()
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
def query_tab(tbl_obj, query=None):
	
	return tbl_obj.find(query)

