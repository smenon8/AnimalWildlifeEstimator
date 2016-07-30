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
from collections import OrderedDict
importlib.reload(Features)

def genUniqueImageListFromMap(mapFlName):
	reader = csv.reader(open(mapFlName,"r"))
	head = reader.__next__()
	data = []
	for row in reader:
	    data.append(row)

	images = []
	for row in data:
		images += row[1:len(row)-1]

	uniqueImgs = list(set(images))

	return uniqueImgs

def genAlbumGIDDictFromMap(mapFlName):
	reader = csv.reader(open(mapFlName,"r"))
	head = reader.__next__()
	data = {}

	for row in reader:
		data[row[0]] = row[1:]

	return data

def genImgAlbumDictFromMap(mapFLName):
	uniqImgs = genUniqueImageListFromMap(mapFLName)
	albumImg = genAlbumGIDDictFromMap(mapFLName)

	imgAlbum = {}
	for img in uniqImgs:
	    for album in albumImg.keys():
	        if img in albumImg[album]:
	            imgAlbum[img] = imgAlbum.get(img,[]) + [album]

	return imgAlbum


def getImageFreqFromMap(inFL):
    imgAlbumDict = genImgAlbumDictFromMap(inFL)

    imgFreq = []
    for img in imgAlbumDict:
        imgFreq.append((img, len(imgAlbumDict[img])))

    imgFreq = sorted(imgFreq,key = lambda x : x[1],reverse = True)

    return imgFreq

def genAidGidDictFromMap(mapFL):
    jsonObj = json.load(open(mapFL,"r"))

    aidGidDict = {}
    for gid in jsonObj:
        if jsonObj[gid][0] != None:
            for aid in jsonObj[gid][0]:
                aidGidDict[aid] = aidGidDict.get(aid,[]) + [gid]

    return aidGidDict

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

def genAidGidTupListFromMap(mapFL):
    jsonObj = json.load(open(mapFL,"r"))

    aidGidTupList = []
    for gid in jsonObj:
        if jsonObj[gid][0] != None:
            for aid in jsonObj[gid][0]:
                aidGidTupList.append((aid,gid))

    return aidGidTupList

def genAidFeatureDictList(mapFL):
    jsonObj = json.load(open(mapFL,"r"))

    aidFeaturesList = []

    for aid in jsonObj.keys():
        featuresDict = {}
        features = jsonObj[aid]
        featuresDict['AID'] = aid
        featuresDict['NID'] = features[0][0]
        featuresDict['INDIVIDUAL_NAME'] = features[1][0]
        featuresDict['SPECIES'] = features[2][0]
        featuresDict['SEX'] = features[3][0]
        featuresDict['AGE'] = features[4][0]
        featuresDict['EXEMPLAR_FLAG'] = features[5][0]
        featuresDict['QUALITY'] = features[6][0]
        featuresDict['VIEW_POINT'] = features[7][0]
        featuresDict['CONTRIBUTOR'] = features[8][0] # newly added on 06/22
        
        aidFeaturesList.append(featuresDict)

    return aidFeaturesList

def genAidFeatureDictDict(mapFL):
    jsonObj = json.load(open(mapFL,"r"))

    aidFeaturesDict = {}

    for aid in jsonObj.keys():
        featuresDict = {}
        features = jsonObj[aid]
        # featuresDict['AID'] = aid
        featuresDict['NID'] = str(features[0][0])
        featuresDict['INDIVIDUAL_NAME'] = features[1][0]
        featuresDict['SPECIES'] = features[2][0]
        featuresDict['SEX'] = features[3][0]
        featuresDict['AGE'] = features[4][0]
        featuresDict['EXEMPLAR_FLAG'] = str(features[5][0]) # type-casting to string necessary
        featuresDict['QUALITY'] = features[6][0]
        featuresDict['VIEW_POINT'] = features[7][0]
        featuresDict['CONTRIBUTOR'] = features[8][0] # newly added on 06/22

        aidFeaturesDict[aid] = featuresDict

    return aidFeaturesDict

# mapFL - json format (should be in the format {gid: {aid : features}})
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
def createResultDict(jobRangeStart,jobRangeEnd):
    masterDict = OrderedDict()

    for i in range(jobRangeStart,jobRangeEnd+1):
        inFLTitle = "photo_album_" + str(i)
        inFL = "../results/photo_album_" + str(i) + ".results"
        inFLList = []
        with open(inFL,"r") as inp:
            for line in inp:
                inFLList.append(line.replace('"',''))

        resultList = []
        header = inFLList[0].split("\t")
        for line in inFLList[1:]:
            resultList.append(line.split("\t"))

        resultDict = OrderedDict()
        for i in range(0,len(resultList)):
            for j in range(0,len(header)):
                resultDict[header[j]] = resultDict.get(header[j],[]) + [resultList[i][j]]

        keysOfInterest = list(filter(lambda x: re.search("Answer",x),resultDict.keys()))
        newDict = OrderedDict()
        for key in keysOfInterest:
            newDict[key] = resultDict[key]

        masterDict[inFLTitle] = newDict
        
    return masterDict

def imgShareCountsPerAlbum(imgAlbumDict,results):
    imgShareNotShareList = []
    noResponse = []

    for album in results.keys():
        ansDict = results[album]
        for key in ansDict:
            junk,gid = key.split('.')
            
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

# audit script
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