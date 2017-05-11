'''
Author: Sreejith Menon (smenon8@uic.edu)
Date: May 11, 2017

Methods to load data into the IBEIS datastore on the local mongoD instance

'''

import mongod_helper as md
import json, pandas as pd

def add_data(tbl_obj, doc):
	pass


def add_bty_data(client, doc_nm, source):
	bty_tbl_obj = md.mongod_table(client, 'beauty_tab')


def add_exif_data(client, doc_nm, source):
	exif_tbl_obj = md.mongod_table(client, 'exif_tab')

def add_ibeis_data(client, doc_nm, source):
	ibeis_tbl_obj = md.mongod_table(client, 'ibeis_tab')

def __main__():
	client = md.mongod_instance()


	# Load all giraffe flickr data
	add_bty_data(client, "", "flickr")
	add_exif_data(client, "", "flickr")



if __name__ == "__main__":
	__main__()