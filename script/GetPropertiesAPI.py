# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:44:47 2016

Author: Sreejith Menon (smenon8@uic.edu)

Description: Contains methods to extract specific information from IBEIS database through REST-ful API calls
Functionaties: 
    1. getAnnotID(<image gid>) : returns Annotation ID of the image gid
    2. getImageFeature(<annot_id>,<feature>) : returns the feature corresponding to the annotation ID
    3. getContributorGID(<contributor_id>) : returns a list of images (image gid) clicked by the contributor
"""

import urllib.request
import json

ftrNms = {'SPECIES' : 'species_texts', 'AGE' : 'age_months_est', 'INDIVIDUAL_NAME' : 'nids' , 'SEX' : 'sex_texts',
             'EXEMPLAR_FLAG':'exemplar_flags', 'QUALITY' : 'quality_texts', 'VIEW_POINT' : 'yaw_texts'}
             
# Argument : GID of a single image
# Returns : Corresponding Annotation ID of the GID
def getAnnotID(gid):
    url = "http://pachy.cs.uic.edu:5000/api/image/aids/?gid_list=["+str(gid)+"]"
    response = urllib.request.urlopen(url)
    responseData = response.read().decode('utf-8')
    jsonObj = json.loads(responseData)

    if len(jsonObj['response'][0]) != 0:
        return jsonObj['response'][0]
    else:
        return None
        
# Arguments : Annotation ID , Required Feature
# Accepted Features: species_texts, age_months_est, exemplar_flags, sex_texts, yaw_texts, quality_texts,image_contributor_tag
# Returns : Returns the feature
def getImageFeature(aid,feature):
    url = "http://pachy.cs.uic.edu:5000/api/annot/" + feature + "/?aid_list=[" + str(aid) + "]"
    response = urllib.request.urlopen(url)
    responseData = response.read().decode('utf-8')
    jsonObj = json.loads(responseData)

    return jsonObj['response']


# Arguments : Contributor ID
# Returns : A list of the images(image GID) contributed by the contributor
def getContributorGID(cid):
    url = "http://pachy.cs.uic.edu:5000/api/contributor/gids/?contrib_rowid_list=["+str(cid)+"]"
    response = urllib.request.urlopen(url)
    responseData = response.read().decode('utf-8')
    jsonObj = json.loads(responseData)

    return jsonObj['response'][0]

def getAgeFeatureReadableFmt(ageList):
    if ageList[0] == [-1,-1] or ageList[0] == [None,2] or ageList[0] == [3, 5] or ageList[0] == [6, 11]:
        return ["infant"]
    elif ageList[0] == [12,23]:
        return ["juvenille, one year old"]
    elif ageList[0] == [24,35]:
        return ["juvenille, two year old"]
    elif ageList[0] == [36,None]:
        return ["adult"]
    else:
        return ["unknown"]

def __main__():
    print(getAnnotID(6526))
    #print(getContributorGID(1))
    print(getImageFeature(8810,"exemplar_flags"))
    # ages = [9448, 15613]
    # for a in ages:
    #     print(getImageFeature(a,"age_months_est"))

if __name__ == "__main__":
    __main__()