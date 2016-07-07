# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:44:47 2016

Author: Sreejith Menon (smenon8@uic.edu)

Description: Contains methods to extract specific information from IBEIS database through REST-ful API calls
Functionaties: 
    1. getAnnotID(<image gid>) : returns Annotation ID of the image gid
    2. getImageFeature(<annot_id>,<feature>) : returns the feature corresponding to the annotation ID
    3. getContributorGID(<contributor_id>) : returns a list of images (image gid) clicked by the contributor
    4. getAgeFeatureReadableFmt(<age from IBEIS API> : returns a human readable age)
"""

import requests
import json

ftrNms = {'SPECIES' : 'species_texts', 'AGE' : 'age_months_est', 'INDIVIDUAL_NAME' : 'nids' , 'SEX' : 'sex_texts',
             'EXEMPLAR_FLAG':'exemplar_flags', 'QUALITY' : 'quality_texts', 'VIEW_POINT' : 'yaw_texts'}

baseurl = 'http://pachy.cs.uic.edu:5000'

# Argument : GID of a single image
# Returns : Corresponding Annotation ID of the GID
def getAnnotID(gid):
    response = requests.get(baseurl + '/api/image/annot/rowid/', data = dict(gid_list=[gid]))
    jsonObj = response.json()

    return jsonObj['response'][0] if len(jsonObj['response'][0]) != 0 else None
        
# Arguments : Annotation ID , Required Feature
# Accepted Features: species_texts, age_months_est, exemplar_flags, sex_texts, yaw_texts, quality_texts,image_contributor_tag
# Returns : Returns the feature
def getImageFeature(aid,feature):
    response = requests.get(baseurl + '/api/annot/' + feature + '/', data = dict(aid_list=[aid]))
    jsonObj = response.json()

    return jsonObj['response']

# Arguments : Contributor ID
# Returns : A list of the images(image GID) contributed by the contributor
def getContributorGID(cid):
    url = "http://pachy.cs.uic.edu:5000/api/contributor/gids/?contrib_rowid_list=["+str(cid)+"]"
    response = requests.get(baseurl + '/api/contributor/gids/', data = dict(contrib_rowid_list=[cid]))
    jsonObj = response.json()

    return jsonObj['response'][0]

# Age in IBEIS is stored as a list (an estimated range in months). 
# IBEIS identifies the age of the animal up to 3 years. 
# The animals will be classified as Infants, a year-old juveniles, two year old juveniles or fully grown adults. 
def getAgeFeatureReadableFmt(ageList):
    if ageList[0] == [-1,-1] or ageList[0] == [None,2] or ageList[0] == [3, 5] or ageList[0] == [6, 11]:
        return ["infant"]
    elif ageList[0] == [12,23]:
        return ["juveniles - one year old"]
    elif ageList[0] == [24,35]:
        return ["juveniles- two year old"]
    elif ageList[0] == [36,None]:
        return ["adult"]
    else:
        return ["unknown"]

def __main__():
    for i in range(1,11):
        print(getImageFeature(getAnnotID(i),"age/months")) # age
        print(getImageFeature(getAnnotID(i),"yaw/text")) # yaw_texts
        print(getImageFeature(getAnnotID(i),"exemplar")) # exemplar flag
        print(getImageFeature(getAnnotID(i),"quality/text")) # quality
        print(getImageFeature(getAnnotID(i),"sex/text")) # sex
        print(getImageFeature(getAnnotID(i),"species/text")) # species
        print(getImageFeature(getAnnotID(i),"name/rowid")) # NID
        print(getImageFeature(getAnnotID(i),"name/text")) # Individual Name


if __name__ == "__main__":
   __main__()
   #pass