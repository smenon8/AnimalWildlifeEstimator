'''
Author: Sreejith Menon (smenon8@uic.edu)
Date: May 11, 2017

Methods to load data into the IBEIS datastore on the local mongoD instance

'''

import mongod_helper as md
import DataStructsHelperAPI as DS, importlib, json
importlib.reload(md) 
importlib.reload(DS) 

'''
    This decorator is designed to take care of the GZC and GGR dataset.
    GZC and GGR we don't really need to know the file names, but UNIFORM representation sake
'''
def create_data_decorator(create_data_fnc):
    def wrapper(*args, **kwargs):
        if not args[0]:
            print("No map file found")
            doc = DS.json_loader(args[1])
            tmp_map = {key : key for key in doc.keys()}
            tmp_fl_nm = "/tmp/map_fl.tmp.json"
            with open(tmp_fl_nm, "w") as tmp_fl:
                json.dump(tmp_map, tmp_fl, indent=4)

            return create_data_fnc(tmp_fl_nm, args[1], args[2])
        else:
            return create_data_fnc(*args)

    return wrapper

@create_data_decorator
def create_data(map_fl_nm, doc_nm, source):
    map_obj = DS.flipKeyValue(DS.json_loader(map_fl_nm))
    data_dct = DS.json_loader(doc_nm)

    ld_rdy_doc = {}
    for key in map_obj.keys():
        inner_dct = data_dct.get(key)
        inner_dct.update({"_id" : key})
        inner_dct.update({"gid" : map_obj[key]})
        inner_dct.update({"source" : source})

        ld_rdy_doc[key] = inner_dct

    return ld_rdy_doc



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


    # Load all zebra flickr data
    add_bty_data(client, "../data/flickr_imgs_gid_flnm_map.json",
                "../data/Flickr_Beauty_features.json",
                "flickr_zebra")

    add_exif_data(client, "../data/flickr_imgs_gid_flnm_map.json",
                "../data/Flickr_EXIF_full.json",
                "flickr_zebra")



    # Load GZC beauty features
    add_bty_data(client, None, 
                "../data/GZC_beauty_features.json",
                "GZC")

    # Load GGR beauty features
    add_bty_data(client, None, 
                "../data/ggr_beauty_features.json",
                "GGR")

if __name__ == "__main__":
	__main__()