import mongod_helper as mh


def genGidAidDictFromDB(client, source):
    gid_aid_tbl_obj = mh.mongod_table("ibeis_gid_annot_tab", source)


def extractImageFeaturesFromMap(client, feature, source="GZC"):
    pass