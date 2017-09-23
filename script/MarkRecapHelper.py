# Mark Recapture Helper Scripts
import json
import DeriveFinalResultSet as DRS, mongod_helper as mh
import DataStructsHelperAPI as DS
import importlib
import pandas as pd
import warnings
import sys, math

importlib.reload(mh)


def PRINT(jsonLike):
    print(json.dumps(jsonLike, indent=4))

def genNidMarkRecapDict(mongo_client, source, days_dict, filter_species=None):
    exif_tab_obj = mh.mongod_table(mongo_client, "exif_tab", source)

    cursor = exif_tab_obj.query(cols=['date'])

    img_dt_dict = mh.key_val_converter(cursor, 'date')
    # population estimation using GGR and GZC datasets are done using dates
    if source in ["GZC", "GGR"]:
        img_dt_dict = {gid: DS.getDateFromStr(img_dt_dict[gid], '%Y-%m-%d %H:%M:%S', '%Y-%m-%d') for gid in img_dt_dict.keys()}
    else:
        ''' 
        generally, for population estimation using Flickr/Bing images, the images were divided into annual epochs,
        this could change and in that case the below line should be modified
        '''
        img_dt_dict = {gid: DS.getDateFromStr(img_dt_dict[gid], '%Y-%m-%d %H:%M:%S', '%Y') for gid in img_dt_dict.keys()}


    # Retain only the gids for the dates in the days_dict
    filtered_gid = list(filter(lambda x: img_dt_dict[x] in days_dict.keys(), img_dt_dict.keys()))
    gid_days_num = {gid: days_dict[img_dt_dict[gid]] for gid in filtered_gid}


    gid_nid = DRS.getCountingLogic(mongo_client, "NID", source, False, mongo=True)

    if filter_species != None:
        try:
            gid_species = DRS.getCountingLogic(mongo_client, "SPECIES", source, False, mongo=True)
        except Exception as e:
            print("Exception occured at counting logic step")
            print(e)
            return

        gid_days_num = {gid: gid_days_num[gid] for gid in gid_days_num if
                      gid in gid_species.keys() and filter_species in gid_species[gid]}

    nidMarkRecap = {}
    for gid in gid_days_num.keys():  # only iterate over the GIDs of interest
        if gid in gid_nid.keys():  # not all images with valid EXIF feature will have an annotation
            for nid in gid_nid[gid]:
                if int(nid) > 0:  # and int(nid) != 45: # ignore all the false positives --and ignore NID 45
                    nidMarkRecap[nid] = nidMarkRecap.get(nid, []) + [gid_days_num[gid]]

    nidMarkRecapSet = {nid: list(set(nidMarkRecap[nid])) for nid in nidMarkRecap.keys()}

    return nidMarkRecapSet



# Return Petersen-Lincoln Index for mark-recapture
def applyMarkRecap(nidMarkRecapSet):

    uniqueIndsDay1 = {nid for nid in nidMarkRecapSet if 1 in nidMarkRecapSet[nid]}
    uniqueIndsDay2 = {nid for nid in nidMarkRecapSet if 2 in nidMarkRecapSet[nid]}

    marks = len(uniqueIndsDay1)
    recaptures = len(uniqueIndsDay1 & uniqueIndsDay2)
    day2_sights = len(uniqueIndsDay2)
    try:
        population = day2_sights * marks / recaptures
        confidence = 1.96 * math.sqrt(marks ** 2 * day2_sights * (day2_sights - recaptures) / recaptures ** 2)
    except:
        warnings.warn("There are no recaptures for this case.")
        population = 0
        confidence = 0

    return marks, recaptures, population, confidence


def genSharedGids(gidList, gidPropMapFl, shareData='proportion', probabThreshold=1):
    df = pd.DataFrame.from_csv(gidPropMapFl)

    if shareData == 'proportion':
        gidPropDict = df['Proportion'].to_dict()
        highSharedGids = {str(gid) for gid in gidPropDict.keys() if float(gidPropDict[gid]) >= 80.0}
    else:
        gidShrDict = df['share'].to_dict()
        highSharedGids = {str(gid) for gid in gidShrDict.keys() if float(gidShrDict[gid]) >= probabThreshold}

    return list(set(gidList) & highSharedGids)


def runMarkRecap(source, days_dict, filter_species=None):
    client = mh.mongod_instance()

    return applyMarkRecap(genNidMarkRecapDict(client, source, days_dict, filter_species=filter_species))


if __name__ == "__main__":
    client = mh.mongod_instance()
    source = "flickr_giraffe"
    days_dict = {'2014':1, "2015" : 2}

    print(genNidMarkRecapDict(client, source, days_dict, filter_species="giraffe_reticulated"))