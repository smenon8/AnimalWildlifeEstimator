# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:44:47 2016

@author: sreejithmenon
"""

import urllib.request
import json

# Argument : GID of a single image
# Returns : Annotation ID
def getAnnotID(gid):
    url = "http://pachy.cs.uic.edu:5000/api/image/aids/?gid_list=["+str(gid)+"]"
    response = urllib.request.urlopen(url)
    responseData = response.read().decode('utf-8')
    jsonObj = json.loads(responseData)

    if len(jsonObj['response'][0]) != 0:
        return jsonObj['response'][0][0]
    else:
        return None
        
# Argument : Annotation ID , Required Feature String
# Returns : Returns the feature - tested for species_texts, age_months_est, exemplar_flags, sex_texts, yaw_texts and quality_texts
def getImageFeature(aid,feature):
    url = "http://pachy.cs.uic.edu:5000/api/annot/" + feature + "/?aid_list=["+str(aid)+"]"
    response = urllib.request.urlopen(url)
    responseData = response.read().decode('utf-8')
    jsonObj = json.loads(responseData)

    return jsonObj['response'][0]


def getContributorGID(cid):
    url = "http://pachy.cs.uic.edu:5000/api/contributor/gids/?contrib_rowid_list=["+str(cid)+"]"
    response = urllib.request.urlopen(url)
    responseData = response.read().decode('utf-8')
    jsonObj = json.loads(responseData)

    return jsonObj['response'][0]

def __main__():
    print(getContributorGID(1))
    print(getImageFeature(93,"species_texts"))

if __name__ == "__main__":
    __main__()
# http://pachy.cs.uic.edu:5000/api/annot/qualities/?aid_list=[13390]