# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:44:47 2016

Author: Sreejith Menon (smenon8@uic.edu)

Description: Contains methods to extract specific information from IBEIS database through REST-ful API calls
Functionalaties: 
    1. getAnnotID(<image gid>) : returns Annotation ID of the image gid
    2. getImageFeature(<annot_id>,<feature>) : returns the feature corresponding to the annotation ID
    3. getContributorGID(<contributor_id>) : returns a list of images (image gid) clicked by the contributor
    4. getAgeFeatureReadableFmt(<age from IBEIS API> : returns a human readable age)
"""

import requests, datetime, urllib

ftrNms = {'SPECIES' : 'species_texts', 'AGE' : 'age_months_est', 'INDIVIDUAL_NAME' : 'nids' , 'SEX' : 'sex_texts',
             'EXEMPLAR_FLAG':'exemplar_flags', 'QUALITY' : 'quality_texts', 'VIEW_POINT' : 'yaw_texts'}

baseurl = 'http://pachy.cs.uic.edu:5001/'
ggr_base = 'http://lev.cs.rpi.edu:8080/ggr/ia'

# Argument : GID of a single image
# Returns : Corresponding Annotation ID of the GID
def getAnnotID(gid):
    response = requests.get(baseurl + 'api/image/annot/rowid/', data = dict(gid_list=[gid]))
    jsonObj = response.json()

    return jsonObj['response'][0] if len(jsonObj['response']) != 0 else None
        
# Arguments : Annotation ID , Required Feature
# Accepted Features: species_texts, age_months_est, exemplar_flags, sex_texts, yaw_texts, quality_texts,image_contributor_tag
# Returns : Returns the feature
def getImageFeature(aidList,feature):
    response = requests.get(baseurl + 'api/annot/' + feature + '/?aid_list=' + str(aidList))
    jsonObj = response.json()

    return jsonObj['response']

# Arguments : GID of an image, required EXIF feature
# This method should be used for extracting the exif information of a picture.
def getExifData(gidList,exifFtr):
    response = requests.get(baseurl + 'api/image/' + exifFtr +'/?gid_list='+ str(gidList))
    jsonObj = response.json()

    return jsonObj['response']

# Arguments : Contributor ID
# Returns : A list of the images(image GID) contributed by the contributor

def getContributorGID(cid):
    response = requests.get(baseurl + 'api/contributor/image/rowid/', data = dict(contributor_rowid_list=[cid]))
    jsonObj = response.json()

    return jsonObj['response'][0]

# Age in IBEIS is stored as a list (an estimated range in months). 
# IBEIS identifies the age of the animal up to 3 years. 
# The animals will be classified as Infants, a year-old juveniles, two year old juveniles or fully grown adults. 
def getAgeFeatureReadableFmt(ageList):
    if ageList == [-1,-1] or ageList == [None,2] or ageList == [3, 5] or ageList == [6, 11]:
        return "infant"
    elif ageList == [12,23]:
        return "juveniles - one year old"
    elif ageList == [24,35]:
        return "juveniles- two year old"
    elif ageList == [36,None]:
        return "adult"
    else:
        return "unknown"

# Method for converting unix times into human readable format. 
# Current return format: YYYY-MM-DD HH-mm-ss
# Modified to take into consideration daylight saving changes (now uses utcfromtimestamp method)
def getUnixTimeReadableFmt(unixtm):
    return datetime.datetime.utcfromtimestamp(int(unixtm)).strftime('%Y-%m-%d %H:%M:%S')

# Method for executing GET request for the GGR dataset
def ggr_get(passthru, arg=None):
    if arg:
        url = ggr_base + "?passthru=" + passthru + "&arg=" + arg
    else:
        url = ggr_base + "?passthru=" + passthru

    response = requests.get(url)

    return response.json()

ggr_annot_form_arg = lambda x : urllib.parse.quote('annot_uuid_list=') + '[{' + urllib.parse.quote('"__UUID__"') + ':' + urllib.parse.quote('\"%s\"' %x) + '}]'
ggr_image_form_arg = lambda x : urllib.parse.quote('image_uuid_list=') + '[{' + urllib.parse.quote('"__UUID__"') + ':' + urllib.parse.quote('\"%s\"' %x) + '}]'
ggr_gid_form_arg = lambda x : urllib.parse.quote('gid_list=') + '[' + urllib.parse.quote('\"%s\"' %x)  + ']'

def __main__():
    for i in range(1,2):
        print(getAnnotID(i))
        # print(getImageFeature(getAnnotID(i),"bbox")) # age
        # print(getImageFeature(getAnnotID(i),"yaw/text")) # yaw_texts
        # print(getImageFeature(getAnnotID(i),"exemplar")) # exemplar flag
        # print(getImageFeature(getAnnotID(i),"quality/text")) # quality
        # print(getImageFeature(getAnnotID(i),"sex/text")) # sex
        # print(getImageFeature(getAnnotID(i),"species/text")) # species
        print(getImageFeature(getAnnotID(i),"note")) # NID
        print(getImageFeature(getAnnotID(i),"name/text")) # Individual Name
        print(getImageFeature(getAnnotID(i),"uuid")) # annot UUID
        #print(getImageFeature(getAnnotID(i),"image/contributor/tag")) # Image contributor Tag

    # print(getExifData([1,2,3],'unixtime'))
    # print(getExifData([1],'unixtime'))
    # print(getExifData([2,3],'unixtime'))
    # print(getExifData(1,'lat'))
    # print(getExifData(1,'lon'))

if __name__ == "__main__":
    __main__()


    #pass
    # gidList = "6a92790b-1c2a-301c-6e7d-def645dca1f5"
    # gidList = 1
    # response = requests.get(baseurl + '/api/image/' + "imageset/uuid" +'/?gid_list='+ str(gidList))
    # response = requests.get(baseurl + '/api/annot/image/contributor/tag/json/' , 
    #                     data = dict(annot_uuid_list=[{"__UUID__" : "8b595dc0-9c5a-4caf-9703-9f8ff017e824"}]))
    # jsonObj = response.json()

    # print(jsonObj)