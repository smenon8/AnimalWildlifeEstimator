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
# Accepted Features: species_texts, age_months_est, exemplar_flags, sex_texts, yaw_texts, quality_texts
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

def __main__():
    print(getAnnotID(6526))
    #print(getContributorGID(1))
    #print(getImageFeature(93,"species_texts"))

if __name__ == "__main__":
    __main__()