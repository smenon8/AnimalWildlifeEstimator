'''
Author: Sreejith Menon (smenon8@uic.edu)
Date: May 11, 2017

Methods to load data into the IBEIS datastore on the local mongoD instance

'''

import mongod_helper as md
import json, DataStructsHelperAPI as DS

def create_data(map_fl_nm, doc_nm, source):
    map_obj = DS.flipKeyValue(json_loader(map_fl_nm))
    data_dct = json_loader(doc_nm)

    ld_rdy_doc = {}
    for key in map_obj.keys():
        inner_dct = data_dct.get(key)
        inner_dct.update({"_id" : key})
        inner_dct.update({"gid" : map_obj[key]})
        inner_dct.update({"source" : source})

        ld_rdy_doc[key] = inner_dct

    return ld_rdy_doc

def json_loader(doc_nm):
	with open(doc_nm, "r") as doc:
		return json.load(doc)

def add_bty_data(client, map_fl_nm, doc_nm, source):
	bty_tbl_obj = md.mongod_table(client, 'beauty_tab')

	doc_ld_rdy = create_data(map_fl_nm, doc_nm, source)
	bty_tbl_obj.add_data(doc_ld_rdy)

	return 0

def add_exif_data(client, map_fl_nm, doc_nm, source):
    exif_tbl_obj = md.mongod_table(client, 'exif_tab')
    doc_ld_rdy = create_data(map_fl_nm, doc_nm, source)

    exif_tbl_obj.add_data(doc_ld_rdy)

    return 0

def add_ibeis_data(client, map_fl_nm, doc_nm, source):
    ibeis_tbl_obj = md.mongod_table(client, 'ibeis_tab')

def __main__():
    client = md.mongod_instance()


	# Load all giraffe flickr data
    add_bty_data(client, "../data/Flickr_Giraffes_imgs_gid_flnm_map.json",
                "../data/Flickr_Bty_Giraffe.json",
                "flickr_giraffe")


    add_exif_data(client, "../data/Flickr_Giraffes_imgs_gid_flnm_map.json",
                "../data/Flickr_Giraffe_EXIF.json",
                "flickr_giraffe")


    add_bty_data(client, "../data/flickr_imgs_gid_flnm_map.json",
                "../data/Flickr_Beauty_features.json",
                "flickr_zebra")

    add_exif_data(client, "../data/flickr_imgs_gid_flnm_map.json",
                "../data/Flickr_EXIF_full.json",
                "flickr_zebra")

if __name__ == "__main__":
	__main__()