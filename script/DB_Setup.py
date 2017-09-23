'''
Author: Sreejith Menon (smenon8@uic.edu)
Date: May 11, 2017

Methods to load data into the IBEIS datastore on the local mongoD instance

'''

import mongod_helper as md
import DataStructsHelperAPI as DS, importlib, json

importlib.reload(md)
importlib.reload(DS)

def PRINT(jsonLike):
    print(json.dumps(jsonLike, indent=4))

'''
    This decorator is designed to take care of the GZC and GGR dataset.
    GZC and GGR we don't really need to know the file names, but UNIFORM representation sake
'''
def create_data_decorator(create_data_fnc):
    def wrapper(*args, **kwargs):
        if not args[0]:
            print("No map file found")
            doc = DS.json_loader(args[1])
            tmp_map = {key: key for key in doc.keys()}
            tmp_fl_nm = "/tmp/map_fl.tmp.json"
            with open(tmp_fl_nm, "w") as tmp_fl:
                json.dump(tmp_map, tmp_fl, indent=4)

            return create_data_fnc(tmp_fl_nm, args[1], args[2], args[3])
        else:
            return create_data_fnc(*args)

    return wrapper

'''
    Create data makes sure we have a common representation of the data across different tables. 
    You may use the same function across different tables for all the data-sets currently available.
'''

@create_data_decorator
def create_data(map_fl_nm, doc_nm, key_str, source):
    map_obj =  DS.flipKeyValue(DS.json_loader(map_fl_nm)) # makes it filename : gid mapping

    data_dct = DS.json_loader(doc_nm) # aid features mapping

    ld_rdy_doc = {}
    for key in map_obj.keys(): # keys would be file names
        inner_dct = data_dct.get(key)
        if isinstance(inner_dct, dict):
            if inner_dct:
                inner_dct.update({"_id": key})
                inner_dct.update({key_str: map_obj[key]})
                inner_dct.update({"source": source})
        else:
            temp_dct = {}
            temp_dct["aid"] = inner_dct
            temp_dct.update({"_id": key})
            temp_dct.update({key_str: map_obj[key]})
            temp_dct.update({"source": source})

            inner_dct = temp_dct

        ld_rdy_doc[key] = inner_dct

    return ld_rdy_doc

def add_data_tab(tbl_obj, map_fl_nm, doc_nm, key_str, source):
    doc_ld_rdy = create_data(map_fl_nm, doc_nm, key_str, source)

    # PRINT(doc_ld_rdy)
    tbl_obj.add_data(doc_ld_rdy)

    return 0

def add_bty_data(client, map_fl_nm, doc_nm, source):
    bty_tbl_obj = md.mongod_table(client, 'beauty_tab', source)
    add_data_tab(bty_tbl_obj, map_fl_nm, doc_nm, "gid", source)

    return 0


def add_exif_data(client, map_fl_nm, doc_nm, source):
    exif_tbl_obj = md.mongod_table(client, 'exif_tab', source)
    add_data_tab(exif_tbl_obj, map_fl_nm, doc_nm, "gid", source)

    return 0

'''
    map_fl will be stored separately in a different table (this is basically gid : annotation) - retrieval might be a challenge
    The original table will use annotation id as the key
    
    
    Parameter description : 
    @param client: mongo client
    @param map_fl_nm: gid : filename.jpeg mapping
    @param map_doc_nm: gid : aid mapping
    @param doc_nm: aid : features mapping
    @param source: name of source
'''
def add_ibeis_data(client, map_fl_nm, map_doc_nm, doc_nm, source):
    # add aid feature mapping
    ibeis_annot_ftr_tbl_obj = md.mongod_table(client, 'ibeis_annot_ftr_tab', source)
    add_data_tab(ibeis_annot_ftr_tbl_obj, None, doc_nm, "aid", source)

    # add gid aid mapping
    ibeis_gid_annot_tbl_obj = md.mongod_table(client, 'ibeis_gid_annot_tab', source)
    add_data_tab(ibeis_gid_annot_tbl_obj, None, map_doc_nm, "gid", source)

    return 0


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

    # Load GZC features
    add_bty_data(client, None,
                 "../data/GZC_beauty_features.json",
                 "GZC")

    add_exif_data(client, None,
                  "../data/GZC_EXIF.json",
                  "GZC")

    # Load GGR features
    add_bty_data(client, None,
                 "../data/ggr_beauty_features.json",
                 "GGR")

    add_exif_data(client, None,
                  "../data/GGR_EXIF.json",
                  "GGR")

    add_ibeis_data(client, None, "../data/GZC_gid_aid.json",
                                 "../data/GZC_aid_ftrs.json",
                   "GZC"
                   )

if __name__ == "__main__":
    # __main__()
    client = md.mongod_instance()
    # # client.reset()
    # #
    add_ibeis_data(client,
                   "../gold_set/Flickr_Giraffes_imgs_gid_flnm_map.json",
                   "../gold_set/Flickr_IBEIS_Giraffe_Ftrs_gid_aid_map.json",
                   "../gold_set/Flickr_IBEIS_Giraffe_Ftrs_aid_features.json",
                   "flickr_giraffe"
                   )
    #
    # add_ibeis_data(client,
    #                "../data/Flickr_Giraffes_imgs_gid_flnm_map.json",
    #                "../data/Flickr_IBEIS_Giraffe_Ftrs_gid_aid_map.json",
    #                "../data/Flickr_IBEIS_Giraffe_Ftrs_aid_features.json", "Flickr_giraffe")

    # add_exif_data(client, "../gold_set/Flickr_Giraffes_imgs_gid_flnm_map.json",
    #               "../gold_set/Flickr_Giraffe_EXIF.json",
    #               "flickr_giraffe")