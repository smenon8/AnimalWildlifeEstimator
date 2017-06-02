'''
Author: Sreejith Menon (smenon8@uic.edu)
Date: May 10, 2017

	* Methods to interface with an instance of mongod database
	* Can be modified to connect to any mongod instance and perform basic operations
	* Methods to drop table, modify database etc. planned to be written in the future.
'''

from pymongo import MongoClient, errors
import sys, datetime

# added for future

params = {
    'db_name': 'AWESOME_DS',
    'maxSevSelDelay': 1,
    'log_fl': "/tmp/mongo_instance.live.log"
}


class mongod_instance:
    def __init__(self, conn_cfg=params):
        self.client = MongoClient(serverSelectionTimeoutMS=conn_cfg.get('maxSevSelDelay', 1))
        self.check_mongod_running()
        self.db = self.client[conn_cfg.get("db_name")]
        self.log_fl = conn_cfg.get("log_fl")

        with open(self.log_fl, "a") as log_fl:
            log_fl.write("New instance created at %s\n" % str(datetime.datetime.now()))

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

    def __init__(self, mongod_obj, tbl_nm, source):
        if mongod_obj.is_alive():
            self.db_obj = mongod_obj.get_mongod_db()
            self.tbl = self.db_obj.get_collection(tbl_nm)
            self.tbl_str = tbl_nm
            self.log_fl = mongod_obj.log_fl
            self.source = source

    def get_table(self):
        return self.tbl

    def __str__(self):
        return self.tbl_str

    '''
        Creates works only when the table tbl_nm does not exist
        Once created, it adds the document specified by doc(JSON expected) to the table
        Caution: Exception handling done per row, does not stop if there is a bad record. 
    '''

    def add_data(self, doc):

        fail_count = 0
        failed_keys = []
        for key in doc.keys():
            try:
                self.tbl.insert(doc.get(key))
            except Exception:
                fail_count += 1
                failed_keys.append(key)

        failed_keys.append("\n")
        print("Data added successfully with %d insert failures" % fail_count)

        if fail_count:
            with open(self.log_fl, "a") as log:
                log.write("\n".join(failed_keys))
        return 0

    '''
        Expects MongoD table object and a query in dict/BSON format
        Returns a cursor which is an iterable
    '''

    def query(self, query_obj=None, cols = []):
        if query_obj:
            query_obj.update({'source' : self.source})
        else:
            query_obj = {'source' : self.source}

        col_dict = {}
        if len(cols):
            for col in cols:
                col_dict[col] = 1

        try:
            assert(self.check_tbl_exist())
        except AssertionError as e:
            print("Table does not exist in the database")
            print(e)
            sys.exit(-2)

        if col_dict:
            return self.tbl.find(query_obj, col_dict)
        else:
            return self.tbl.find(query_obj)

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

'''
    This method will iterate through the cursor object that find returns 
'''
def result_iterator(cursor_obj):
    try:
        assert(cursor_obj.count() != 0)
    except AssertionError as e:
        print("Empty cursor. No records found.")
        sys.exit(-2)

    result_obj = {}
    while cursor_obj.alive:
        obj = cursor_obj.next()
        key = obj.get("_id")
        obj.pop("_id")

        result_obj[key] = obj

    return result_obj

'''
    Easy access method to return result in the form of gid : column 
'''
def key_val_converter(cursor_obj, col_nm):
    result = {}
    while cursor_obj.alive:
        next_obj = cursor_obj.next()

        result[next_obj.get("_id")] = next_obj.get(col_nm)

    return result

def __main__():
    client = mongod_instance()

    print(client.is_alive())
    exif_tbl_obj = mongod_table(client, 'exif_tab', 'flickr_giraffe')

    cursor = exif_tbl_obj.query(query_obj=None, cols=['long', 'lat'])

    print(cursor.count())
    print(result_iterator(cursor))



if __name__ == "__main__":
    __main__()
    # client = mongod_instance()
    # client.reset()