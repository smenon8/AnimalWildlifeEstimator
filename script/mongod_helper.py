'''
Author: Sreejith Menon (smenon8@uic.edu)
Date: May 10, 2017

	* Methods to interface with an instance of mongod database
	* Can be modified to connect to any mongod instance and perform basic operations
	* Methods to drop table, modify database etc. planned to be written in the future.
'''

from pymongo import MongoClient, errors
import sys
# added for future

params = {
	'db_name' : 'AWESOME_DS',
	'maxSevSelDelay' : 1
}

class mongod_instance:
	def __init__(self, conn_cfg=params):
		self.client = MongoClient(serverSelectionTimeoutMS=conn_cfg.get('maxSevSelDelay', 1))
		self.check_mongod_running()
		self.db = self.client[conn_cfg.get("db_name")]

	def check_mongod_running(self, conn_cfg=params):
		try:
			self.client.server_info()
		except errors.ServerSelectionTimeoutError as err:
			print("MongoDB instance has not started or is dead..!")
			self.client = err
			sys.exit(-2)
		return self.client

	def get_mongod_db(self, conn_cfg=params):
		return self.db

	def is_alive(self):
		self.check_mongod_running()
		return True

	def reset(self):
		for collection in self.db.collection_names():
			tbl = self.db[collection]
			tbl.drop()

class mongod_table:
	'''
		Expects MongoD database object and table name tbl_nm as a string
	'''
	def __init__(self, mongod_obj, tbl_nm):
		if mongod_obj.is_alive():
			self.db_obj = mongod_obj.get_mongod_db()
			self.tbl = self.db_obj.get_collection(tbl_nm)
			self.tbl_str = tbl_nm

	def get_table(self):
		return self.tbl

	def __str__(self):
		return self.tbl_str

	'''
		Creates works only when the table tbl_nm does not exist
		Once created, it adds the document specified by doc(JSON expected) to the table
	'''
	def add_data(self, doc):
		try:
			for key in doc.keys():
				self.tbl.insert(doc.get(key))
		except Exception as e:
			print("Insert failure..!")
			print(e)
			print(key)
			sys.exit(-2)


		print("Data added successfully")
		return 0

	'''
		Expects MongoD table object and a query in dict/BSON format
		Returns a cursor which is an iterable
	'''
	def query(self, query_obj=None):
		if self.check_tbl_exist():
			return self.tbl.find(query_obj)
		else:
			print("Table does not exist in the database")
			sys.exit(-2)

	def check_tbl_exist(self):
		if self.tbl_str in self.db_obj.collection_names():
			return True
		else:
			return False

	def drop_table(self):
		if self.check_tbl_exist():
			self.tbl.drop()
		else:
			print("Table does not exist in the database")
			sys.exit(-2)
