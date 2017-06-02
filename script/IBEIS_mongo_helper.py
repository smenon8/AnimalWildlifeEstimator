import mongod_helper as MH


# This method is used to generate the gid:aid map
def genGidAidDictFromDB(client, source):
    gid_aid_tbl_obj = MH.mongod_table(client, "ibeis_gid_annot_tab", source)
    res_obj = MH.result_iterator(gid_aid_tbl_obj.query({}, ['aid']))

    gid_aid_map = {gid :res_obj[gid]['aid'] for gid in res_obj.keys()}

    return gid_aid_map

def extractImageFeaturesFromMap(client, feature, source="GZC"):
    aid_ftr_tbl_obj = MH.mongod_table(client, "ibeis_annot_ftr_tab", source)
    res_obj = MH.result_iterator(aid_ftr_tbl_obj.query({}, [feature]))


    gid_aid_map = genGidAidDictFromDB(client, source)
    gid_ftr = {}
    for gid in gid_aid_map.keys():
        if gid_aid_map[gid][0] != None:
            for aid in gid_aid_map[gid]:
                gid_ftr[gid] = gid_ftr.get(gid, []) + [res_obj[str(aid)][feature]]

    return gid_ftr