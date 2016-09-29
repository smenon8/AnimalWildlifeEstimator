# python-3
# Author: Sreejith Menon (smenon8@uic.edu)
# Creation date: 5/23/16

'''
Script for getting all images without duplicates from the csv file.
Date: May 23, 2016

The mapFlName referred to in the  entire script is : ../data/imageGID_job_map_expt2_corrected.csv
'''

import csv
import BuildConsolidatedFeaturesFile as Features
import importlib
import re
import json
from collections import OrderedDict, Counter
import pandas as pd
import DataStructsHelperAPI as DS
importlib.reload(Features)

# This method is used to generate a list of all images that are used in the current experiment as specified by the map file.
def genUniqueImageListFromMap(mapFlName):
    with open(mapFlName,"r") as csvFl:
        reader = csv.reader(csvFl)
        head = reader.__next__()
        data = [row for row in reader]

    images = [img for row in data for img in row[1:]]

    return list(set(images))

# This method is used to generate a dictionary in the form { Album : [GIDS] }. 
# This object will give us the capability to query which images exist in a particular album.
def genAlbumGIDDictFromMap(mapFlName):
    reader = csv.reader(open(mapFlName,"r"))
    head = reader.__next__()
    data = {row[0] : row[1:] for row in reader}

    return data

# This method is used to generate a dictionary in the form { GID: [Albums] }. 
# This object will give us the capability to query which album contain a particular GID.
def genImgAlbumDictFromMap(mapFLName):
	uniqImgs = genUniqueImageListFromMap(mapFLName)
	albumImg = genAlbumGIDDictFromMap(mapFLName)

	imgAlbum = {}
	for img in uniqImgs:
	    for album in albumImg.keys():
	        if img in albumImg[album]:
	            imgAlbum[img] = imgAlbum.get(img,[]) + [album]

	return imgAlbum

# This method is used to generate a dictionary in the form { GID : No. of albums it appears }. 
def getImageFreqFromMap(inFL):
    imgAlbumDict = genImgAlbumDictFromMap(inFL)
    imgFreq = sorted([(img, len(imgAlbumDict[img])) for img in imgAlbumDict],key = lambda x : x[1],reverse = True)

    return imgFreq

# This method is used to generate a dictionary in the form { AID : GID }.
def genAidGidDictFromMap(mapFL):
    jsonObj = json.load(open(mapFL,"r"))

    aidGidDict = {}
    for gid in jsonObj:
        if jsonObj[gid][0] != None:
            for aid in jsonObj[gid][0]:
                aidGidDict[aid] = aidGidDict.get(aid,[]) + [gid]

    return aidGidDict

# This method is used to generate a dictionary in the form { GID : List of AIDs in that image }.
def genGidAidDictFromMap(mapFL):
    jsonObj = json.load(open(mapFL,"r"))

    gidAidDict = {}
    for gid in jsonObj:
        if jsonObj[gid][0] != None:
            for aid in jsonObj[gid][0]:
                gidAidDict[gid] = gidAidDict.get(gid,[]) + [aid]
        else:
            gidAidDict[gid] = None
    
    return gidAidDict

# This method is used to generate  a list of tuples in the form ( AID , GID ).
def genAidGidTupListFromMap(mapFL):
    jsonObj = json.load(open(mapFL,"r"))

    aidGidTupList = []
    for gid in jsonObj:
        if jsonObj[gid][0] != None:
            for aid in jsonObj[gid][0]:
                aidGidTupList.append((aid,gid))

    return aidGidTupList

# This method is used to generate a list of dictionaries in the form [{'AID': xx,'NID' : xx ,.. }]. 
# This object will give us the capability to iterate through all annotations and their respective features.
def genAidFeatureDictList(mapFL):
    jsonObj = json.load(open(mapFL,"r"))

    aidFeaturesList = []

    for aid in jsonObj.keys():
        featuresDict = {}
        features = jsonObj[aid]
        featuresDict['AID'] = aid
        featuresDict['NID'] = features[0]
        featuresDict['INDIVIDUAL_NAME'] = features[1]
        featuresDict['SPECIES'] = features[2]
        featuresDict['SEX'] = features[3]
        featuresDict['AGE'] = features[4]
        featuresDict['EXEMPLAR_FLAG'] = features[5]
        featuresDict['QUALITY'] = features[6]
        featuresDict['VIEW_POINT'] = features[7]
        featuresDict['CONTRIBUTOR'] = features[8] # newly added on 06/22
        
        aidFeaturesList.append(featuresDict)

    return aidFeaturesList

# This method is used to generate a dictionary in the form { AID : {'NID' : xxx , 'SPECIES' : xxx, .. }}. 
# This object will give us the capability to query one/multiple features given a annotation ID.
def genAidFeatureDictDict(mapFL):
    jsonObj = json.load(open(mapFL,"r"))

    aidFeaturesDict = {}

    for aid in jsonObj.keys():
        featuresDict = {}
        features = jsonObj[aid]
        # featuresDict['AID'] = aid
        featuresDict['NID'] = str(features[0])
        featuresDict['INDIVIDUAL_NAME'] = features[1]
        featuresDict['SPECIES'] = features[2]
        featuresDict['SEX'] = features[3]
        featuresDict['AGE'] = features[4]
        featuresDict['EXEMPLAR_FLAG'] = str(features[5]) # type-casting to string necessary
        featuresDict['QUALITY'] = features[6]
        featuresDict['VIEW_POINT'] = features[7]
        featuresDict['CONTRIBUTOR'] = features[8] # newly added on 06/22

        aidFeaturesDict[aid] = featuresDict

    return aidFeaturesDict

def genGidAidFtrDf(gidAidMapFl,aidFtrMapFl,outFlNm="/tmp/genGidAidFtrDf.dump.csv"):
    aidFeaturesDf = pd.DataFrame(genAidFeatureDictList(aidFtrMapFl))
    aidFeaturesDf['AID'] = aidFeaturesDf['AID'].astype('int32')
    
    aidGidDict = genAidGidTupListFromMap(gidAidMapFl)
    aidGidDf= pd.DataFrame(aidGidDict,columns = ['AID','GID'])
    
    df = pd.merge(aidGidDf,aidFeaturesDf,left_on='AID',right_on='AID')
    df.to_csv(outFlNm,index=False)

    return df

# mapFL - json format (should be in the format {gid: {aid : features}})
# This method is used to generate a dictionary in the form { GID : [list of features instances in that image]}. 
# This object will give us the capability to check what feature instances are present in a given image. 
def extractImageFeaturesFromMap(gidAidMapFl,aidFtrMapFl,feature):    
    aidFeatureDict = genAidFeatureDictDict(aidFtrMapFl)
    
    gidAidDict = genGidAidDictFromMap(gidAidMapFl)

    gidFtr = {}
    for gid in gidAidDict:
        if gidAidDict[gid]!= None:
            for aid in gidAidDict[gid]:
                gidFtr[gid] = gidFtr.get(gid,[]) + [aidFeatureDict[str(aid)][feature]]
    
    return gidFtr


# Part 1: Building the results dictionary (all the fields of interest for all the available jobs)
# Returns a master dictionary that has job: answers key-value pair. 
# Every album corresponds to a .result file which is extracted from the Amazon Mechanical Turk interface. 
# This method parses the results file and generates a python object consisting of each response key with the actual response from the users. 
# The dictionary is of the form: { photo_album_i : { Answer.GID : [ GID|'share' , 'GID'|'noShare'] }} 
# All the results file from jobRangeStart to jobRangeEnd will be parsed and included in the output object.
def createResultDict(jobRangeStart,jobRangeEnd,workerData=False):
    masterDict = OrderedDict()

    for i in range(jobRangeStart,jobRangeEnd+1):
        inFLTitle = "photo_album_" + str(i)
        inFL = "../results/photo_album_" + str(i) + ".results"
        with open(inFL,"r") as inp:
            inFLList = [line.replace('"','') for line in inp]

        header = inFLList[0].split("\t")
        resultList = [line.split("\t") for line in inFLList[1:]]

        resultDict = OrderedDict()
        for i in range(0,len(resultList)):
            for j in range(0,len(header)):
                resultDict[header[j]] = resultDict.get(header[j],[]) + [resultList[i][j]]

        keysOfInterest = list(filter(lambda x: re.search("Answer",x),resultDict.keys()))
        if workerData:
            keysOfInterest += list(filter(lambda x: re.search("workerid",x),resultDict.keys()))
        newDict = OrderedDict()
        for key in keysOfInterest:
            newDict[key] = resultDict[key]

        masterDict[inFLTitle] = newDict
        
    return masterDict

# Not added to github pages
# This method will be used to extract responses to general questions in the mechanical turk job.
# For instance, in experiment 1 and 2, there were questions asking about how often one shares on social media etc.
def genCntrsGenQues(jobRangeStart,jobRangeEnd,keyList):
    results = createResultDict(jobRangeStart,jobRangeEnd)

    answers = [[ans for album in results.keys() for ans in results[album][key]] for key in keyList]
    cntrObj = {keyList[i] : Counter(answers[i]) for i in range(len(keyList))}

    return cntrObj

# This method is used to generate the list of tags generated by Microsoft Image tagging API, thresholded by confindence. 
# With each tag, there is an associated confidence which quantifies the confidence of the tag prediciting algorithm. 
# For purpose of experiments, the threshold is defaulted to 0.5, any tags predicted with confidence greater than 0.5 is accepted and the rest is rejected.
def genMSAIDataHighConfidenceTags(tagInpDataFl,threshold=0.5):
    with open(tagInpDataFl,"r") as tagInp:
        taggedData = json.load(tagInp)

    gidFtrs = {}
    for gid in taggedData:
        tgs = taggedData[gid]['tags']
        if len(tgs) == 0:
            gidFtrs[gid] = [None]
        for dic in tgs:
            if dic['confidence'] >= threshold: # added for retaining only high confidence tags
                gidFtrs[gid] = gidFtrs.get(gid,[]) + [dic['name']]

    return gidFtrs

# This method returns a Python list which gives us the capability to iterate through all the images, the number of times an image was shared or not shared in a particular album. 
# This object will form the basis of all statistic computations in the project. The format of a tuple inside the list is of the form (GID, Album, Share count, Not Share count, Proportion). 
# The other return object is the list of all (GID, albums) for which there was no valid response. 
# (Form fields in certain albums in experiment 2 were not mandatory in the beginning, the bug was identified and corrected in a later stage.)
def imgShareCountsPerAlbum(imgAlbumDict,results):
    imgShareNotShareList = []
    noResponse = []

    for album in results.keys():
        ansDict = results[album]
        for key in ansDict:
            _,gid = key.split('.')
            
            if gid.isdigit(): # to avoid answers to q1,q2, comments and submit btn
                shrNotShr = ansDict[key]
                shareCount = 0
                notShareCount = 0
                ansOnceFlag = False
                for answer in shrNotShr: 
                    if len(answer.split("|")) == 2:
                        ansOnceFlag = True
                        imgRes,ans = answer.split("|") 
                        if ans == 'share':
                            shareCount +=1
                        else:
                            notShareCount += 1
                    else:
                        imgRes = answer[0]
                        noResponse.append((imgRes,album))
                        
                imgShareNotShareList.append((gid,album,shareCount,notShareCount,shareCount*100/(shareCount+notShareCount)))

    return imgShareNotShareList,noResponse

def createMstrFl(gidAidFtrFl,tagsFlNm,attribList,outFlNm="/tmp/createMstrFl.dump.csv"):
    df = pd.DataFrame.from_csv(gidAidFtrFl)
    df.reset_index(inplace=True)

    df = df[attribList]
    if 'CONTRIBUTOR' in attribList:
        df['CONTRIBUTOR'] = df[['CONTRIBUTOR']].applymap(lambda x : x.replace(',',''))

    df = df.groupby('GID').agg(','.join).reset_index()
    df.GID = df.GID.astype(str) 

    gidFtrsLst = DS.cnvrtDictToLstTup(genMSAIDataHighConfidenceTags(tagsFlNm))
    df_tags = pd.DataFrame(gidFtrsLst,columns=['GID','tags'])
    df_tags['GID'] = df_tags['GID'].astype(str)
    
    df_comb = pd.merge(df,df_tags,left_on='GID',right_on='GID')
    df_comb.to_csv(outFlNm,index=False)

    return df_comb

# audit script
# This method is an audit method that ensures there are no leaks or incorrect data in the result and feature objects. 
# The 3 boolean variables indicate 3 different types of errors.
def auditResMap(imgAlbumDict,resultList):
    err1 = False
    err2 = False
    err3 = False
    imgAlbmDctRest = {}
    
    for tup in resultList:
        imgAlbmDctRest[tup[0]] = imgAlbmDctRest.get(tup[0],[]) + [tup[1]]
            
    for tup in resultList:
        shouldBeInAlbms = imgAlbumDict[tup[0]]
        
        if tup[1] not in shouldBeInAlbms:
            err1 = True

    
    for gid in imgAlbmDctRest.keys():
        albmRes = imgAlbmDctRest[gid]
        albmOri = imgAlbumDict[gid]

        for albm in albmOri:
            if albm not in albmRes:
                err2 = True
        
        for albm in albmRes:
            if albm not in albmOri:
                err3 = True
      
    return err1,err2,err3

def __main__():
    allUniqImgs = genUniqueImageListFromMap("../data/imageGID_job_map_expt2_corrected.csv")
    
    # outFL = "../data/all_imgs_expt2.csv"
    # writeFL = open(outFL,"w")
    # writer = csv.writer(writeFL)

    # writer.writerow(allUniqImgs)

    # writeFL.close()
    
    Features.buildFeatureFl(allUniqImgs,"../data/experiment2.csv",False)

if __name__ == "__main__":
	__main__()
    #pass