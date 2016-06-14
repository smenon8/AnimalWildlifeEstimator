
# coding: utf-8
# python-3

import importlib
import JobsMapResultsFilesToContainerObjs as ImageMap
import pandas as pd
import statistics as s
import re
import GetPropertiesAPI as GP
import matplotlib.pyplot as plt 
import csv
import json
importlib.reload(ImageMap)
importlib.reload(GP)

gidAidMapFl = "../data/experiment2_gid_aid_map.json"
aidFeatureMapFl = "../data/experiment2_aid_features.json"
imgJobMap = "../data/imageGID_job_map_expt2_corrected.csv"

def genTotCnts(ovrCnts):
    dSum = {}
    for key in ovrCnts:
        dSum[key] = sum(ovrCnts[key])
        
    return dSum

def getShrProp(ovrAggCnts) :   
    totCnt = genTotCnts(ovrAggCnts)

    shareKeys = list(filter(lambda x : 'share' in x,totCnt.keys()))
    totKeys = list(filter(lambda x : 'total' in x,totCnt.keys()))

    shareKeys = sorted(shareKeys,key=lambda x: (x[:len(x)-1]))
    totKeys = sorted(totKeys,key=lambda x: (x[:len(x)-1]))

    lenKey = len(shareKeys[0])-1

    propDict = {}
    for i in range(len(shareKeys)):
         propDict[shareKeys[i][:lenKey]] = totCnt[shareKeys[i]] * 100 / totCnt[totKeys[i]]
            
    return propDict

# independent of the results
def getCountingLogic(gidAidMapFl,aidFeatureMapFl,feature,withNumInds=True):
    featuresPerImg = ImageMap.extractImageFeaturesFromMap(gidAidMapFl,aidFeatureMapFl,feature)
    
    countLogic = {}
    for gid in featuresPerImg.keys():
        numInds = len(featuresPerImg[gid]) # number of individuals in a particular image
        countFor = list(set(featuresPerImg[gid]))
        if withNumInds:
            countLogic[gid] = [numInds,countFor]
        else:
            countLogic[gid] = countFor
        
    return countLogic

def genAlbmFtrs(gidAidMapFl,aidFeatureMapFl,imgJobMap,reqdFtrList):
    albmFtrDict = {}
    albumGidDict = ImageMap.genAlbumGIDDictFromMap(imgJobMap)

    for cntFtr in reqdFtrList:
        cntLogic = getCountingLogic(gidAidMapFl,aidFeatureMapFl,cntFtr,False)
        for album in albumGidDict.keys():
            ftrDict = albmFtrDict.get(album,{})
            for gid in albumGidDict[album]:
                ftrList = cntLogic.get(gid,"UNIDENTIFIED")
                if ftrList != "UNIDENTIFIED":
                    for ftr in ftrList:
                        ftrDict[ftr] = ftrDict.get(ftr,0) + 1
                else:
                    ftrDict['UNIDENTIFIED'] = ftrDict.get('UNIDENTIFIED',0) + 1
            albmFtrDict[album] = ftrDict
            
    return albmFtrDict

def getShrPropImgsAcrossAlbms(imgJobMap,resSetStrt,resSetEnd,flNm):
    imgAlbumDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)
    master = ImageMap.createResultDict(resSetStrt,resSetEnd)
    imgShareNotShareList,noResponse = ImageMap.imgShareCountsPerAlbum(imgAlbumDict,master)

    albumGidDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)

    imgsInMultAlbms = list(filter(lambda x : len(albumGidDict[x]) > 1,albumGidDict.keys()))

    gidAlbmDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)


    imgShareNotShareList
    imgAlbmPropDict = {}
    for tup in imgShareNotShareList:
        imgAlbmPropDict[(tup[0],tup[1])] = tup[4]


    consistency = {}
    for gid in imgsInMultAlbms:
        tempDict = {}
        for albm in gidAlbmDict[gid]:
            tempDict[albm] = imgAlbmPropDict.get((gid,albm),None)
        consistency[gid] = tempDict

    fl = open(flNm,"w")
    json.dump(consistency,fl,indent=4)
    fl.close()
    
    return consistency

# verified
def ovrallShrCntsByFtr(gidAidMapFl,aidFeatureMapFl,feature,imgJobMap,resSetStrt,resSetEnd):
    countLogic = getCountingLogic(gidAidMapFl,aidFeatureMapFl,feature)
    imgAlbumDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)
    master = ImageMap.createResultDict(resSetStrt,resSetEnd)
    imgShareNotShareList,noResponse = ImageMap.imgShareCountsPerAlbum(imgAlbumDict,master)
    
    answerSet = {}
    
    for tup in imgShareNotShareList:
        if tup[0] not in countLogic.keys(): # where the image has no associated annotation, tup[0] = GID
            answerSet[('UNIDENTIFIED' , 'share')] = answerSet.get(('UNIDENTIFIED' , 'share'),[]) + [tup[2]]
            answerSet[('UNIDENTIFIED' , 'not_share')] = answerSet.get(('UNIDENTIFIED' , 'not_share'),[]) + [tup[3]]
            answerSet[('UNIDENTIFIED', 'total')] = answerSet.get(('UNIDENTIFIED' , 'total'),[]) + [tup[2] + tup[3]]
        else: 
            logic = countLogic[tup[0]]
            for countForEle in logic[1]:
                varNameShare = (countForEle , "share")
                varNameNotShare = (countForEle , "not_share")
                varNameTot = (countForEle , "total")
                answerSet[varNameShare] = answerSet.get(varNameShare,[]) + [tup[2]]
                answerSet[varNameNotShare] = answerSet.get(varNameNotShare,[]) + [tup[3]]
                answerSet[varNameTot] = answerSet.get(varNameTot,[]) + [tup[2] + tup[3]]
                
    return answerSet


def shrCntsByFtrPrAlbm(gidAidMapFl,aidFeatureMapFl,feature,imgJobMap,resSetStrt,resSetEnd):
    countLogic = getCountingLogic(gidAidMapFl,aidFeatureMapFl,feature)
    imgAlbumDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)
    master = ImageMap.createResultDict(resSetStrt,resSetEnd)
    imgShareNotShareList,noResponse = ImageMap.imgShareCountsPerAlbum(imgAlbumDict,master)
    
    answerSet = {}
    
    for tup in imgShareNotShareList:
        if tup[0] not in countLogic.keys(): # where the image has no associated annotation, tup[0] = GID
            answerSet[('UNIDENTIFIED' , 'share', tup[1])] = answerSet.get(('UNIDENTIFIED' , 'share', tup[1]),[]) + [tup[2]]
            answerSet[('UNIDENTIFIED' , 'not_share', tup[1])] = answerSet.get(('UNIDENTIFIED' , 'not_share', tup[1]),[]) + [tup[3]]
            answerSet[('UNIDENTIFIED', 'total', tup[1])] = answerSet.get(('UNIDENTIFIED' , 'total', tup[1]),[]) + [tup[2] + tup[3]]
        else: 
            logic = countLogic[tup[0]]
            for countForEle in logic[1]:
                varNameShare = (countForEle , tup[1], "share")
                varNameNotShare = (countForEle , tup[1], "not_share")
                varNameTot = (countForEle , tup[1], "total")
                answerSet[varNameShare] = answerSet.get(varNameShare,[]) + [tup[2]]
                answerSet[varNameNotShare] = answerSet.get(varNameNotShare,[]) + [tup[3]]
                answerSet[varNameTot] = answerSet.get(varNameTot,[]) + [tup[2] + tup[3]]
    return answerSet

def ovrallShrCntsByTwoFtrs(gidAidMapFl,aidFeatureMapFl,ftr1,ftr2,imgJobMap,resSetStrt,resSetEnd):
    countLogic1 = getCountingLogic(gidAidMapFl,aidFeatureMapFl,ftr1)
    countLogic2 = getCountingLogic(gidAidMapFl,aidFeatureMapFl,ftr2)

    imgAlbumDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)
    master = ImageMap.createResultDict(resSetStrt,resSetEnd)
    imgShareNotShareList,noResponse = ImageMap.imgShareCountsPerAlbum(imgAlbumDict,master)
    
    answerSet = {}
    unEvnFtrsTups =[]
    for tup in imgShareNotShareList:
        if tup[0] not in countLogic1.keys(): # where the image has no associated annotation, tup[0] = GID
            pass
            answerSet[('UNIDENTIFIED' , None,'share')] = answerSet.get(('UNIDENTIFIED' ,None, 'share'),[]) + [tup[2]]
            answerSet[('UNIDENTIFIED' , None, 'not_share')] = answerSet.get(('UNIDENTIFIED' , None, 'not_share'),[]) + [tup[3]]
            answerSet[('UNIDENTIFIED' , None, 'total')] = answerSet.get(('UNIDENTIFIED' , None, 'total'),[]) + [tup[2]+tup[3]]
        else: 
            logic1 = countLogic1[tup[0]]
            logic2 = countLogic2[tup[0]]
            for i in range(len(logic1[1])):
                if len(logic1[1]) == len(logic2[1]): # there are two individuals with matching features
                    varNameShare = (logic1[1][i] , logic2[1][i], "share")
                    varNameNotShare = (logic1[1][i] , logic2[1][i], "not_share")
                    varNameTot = (logic1[1][i] , logic2[1][i], "total")
                # there are more logic1 features than logic2 features
                elif len(logic1[1]) == 1 or len(logic2[1]) == 1: # one of the logic has just 1 feature
                    if len(logic1[1]) == 1:
                        varNameShare = (logic1[1][0] , logic2[1][i], "share")
                        varNameNotShare = (logic1[1][0] , logic2[1][i], "not_share")
                        varNameTot = (logic1[1][0] , logic2[1][i], "total")
                    else:
                        varNameShare = (logic1[1][i] , logic2[1][0], "share")
                        varNameNotShare = (logic1[1][i] , logic2[1][0], "not_share")
                        varNameTot = (logic1[1][i] , logic2[1][0], "total")
                else: # uneven features in logic1 and logic2
                      unEvnFtrsTups.append(tup)

                answerSet[varNameShare] = answerSet.get(varNameShare,[]) + [tup[2]]
                answerSet[varNameNotShare] = answerSet.get(varNameNotShare,[]) + [tup[3]]
                answerSet[varNameTot] = answerSet.get(varNameTot,[]) + [tup[2] + tup[3]]
          
    # handling un-even features
    unEvnFtrsTups = list(set(unEvnFtrsTups))
    for tup in unEvnFtrsTups:
        aidList = GP.getAnnotID(tup[0])
        for aid in aidList:
            feature1 = GP.getImageFeature(aid,GP.ftrNms[ftr1])
            feature2 = GP.getImageFeature(aid,GP.ftrNms[ftr2])
            
            feature1 = list(map(str,feature1))
            feature2 = list(map(str,feature2))

            if ftr1 == 'AGE':
                feature1 = GP.getAgeFeatureReadableFmt(feature1)
            if ftr2 == 'AGE':
                feature2 = GP.getAgeFeatureReadableFmt(feature2)

            varNameShare = (feature1[0],feature2[0],"share")
            varNameNotShare = (feature1[0],feature2[0],"not_share")
            varNameTot = (feature1[0],feature2[0],"total")
            
            answerSet[varNameShare] = answerSet.get(varNameShare,[]) + [tup[2]]
            answerSet[varNameNotShare] = answerSet.get(varNameNotShare,[]) + [tup[3]]
            answerSet[varNameTot] = answerSet.get(varNameTot,[]) + [tup[2] + tup[3]]
            
    return answerSet

def genNumIndsRankList():
    # no. of individuals per image
    countLogic = getCountingLogic(gidAidMapFl,aidFeatureMapFl,"SPECIES")
    imgAlbumDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)
    master = ImageMap.createResultDict(1,100)
    imgShareNotShareList,noResponse = ImageMap.imgShareCountsPerAlbum(imgAlbumDict,master)

    totOfIndsPerImg = {}
    for key in countLogic:
        totOfIndsPerImg[countLogic[key][0]] = totOfIndsPerImg.get(countLogic[key][0],0) + 1
        
    # Rank list by number of images
    noOfIndsPerImgSharesRnkLst = {}
    noOfIndsPerImgNotSharesRnkLst = {}

    for tup in imgShareNotShareList:
        if tup[0] in countLogic.keys():
            noOfIndsPerImgSharesRnkLst[countLogic[tup[0]][0]] = noOfIndsPerImgSharesRnkLst.get(countLogic[tup[0]][0],0) + tup[2]
            noOfIndsPerImgNotSharesRnkLst[countLogic[tup[0]][0]] = noOfIndsPerImgNotSharesRnkLst.get(countLogic[tup[0]][0],0) + tup[3]

    return noOfIndsPerImgSharesRnkLst,noOfIndsPerImgNotSharesRnkLst

def __main__():

    d = ovrallShrCntsByTwoFtrs(gidAidMapFl,aidFeatureMapFl,"SPECIES","AGE",imgJobMap,1,100)
    #d = shrCntsByFtrPrAlbm(gidAidMapFl,aidFeatureMapFl,"SPECIES",imgJobMap,1,50)
    #d = ovrallShrCntsByFtr(gidAidMapFl,aidFeatureMapFl,"SPECIES",imgJobMap,1,50)

    dc = getShrProp(d)

    pd.DataFrame(dc,index=["share proportion"]).transpose()


    '''
    resultsPerJobDf > Gives you shares/not shares per image per album (Python Object of .results file converted to DF)
    resultsPerJobDf['GID','Album','Shared','Not Shared','Proportion']
    '''
    imgAlbumDict = ImageMap.genImgAlbumDictFromMap("../data/imageGID_job_map_expt2_corrected.csv")
    master = ImageMap.createResultDict(1,100)
    imgShareNotShareList,noResponse = ImageMap.imgShareCountsPerAlbum(imgAlbumDict,master)

    resultsPerJobDf = pd.DataFrame(imgShareNotShareList,columns = ['GID','Album','Shared','Not Shared','Proportion'])

    '''
    Code for reading from json files into data frames
    aidGidDf['AID','GID']
    aidFeaturesDf['AID',[FEATURES]]
    '''
    aidGidDict = ImageMap.genAidGidTupListFromMap('../data/experiment2_gid_aid_map.json')
    aidGidDf= pd.DataFrame(aidGidDict,columns = ['AID','GID'])

    aidFeaturesDf = pd.DataFrame(ImageMap.genAidFeatureDictList('../data/experiment2_aid_features.json'))
    aidFeaturesDf['AID'] = aidFeaturesDf['AID'].astype('int32')

    '''
    rankListImgsDf  > Gives you the results of number of times each image was shared overall
    rankListImgsDf['GID','Shared','Not Shared','Proportion']
    '''
    rankListImgsDf = resultsPerJobDf.groupby(['GID'])['Shared','Not Shared'].sum() 
    rankListImgsDf['Total'] = rankListImgsDf['Shared'] + rankListImgsDf['Not Shared']
    rankListImgsDf['Proportion'] = rankListImgsDf['Shared'] * 100 / rankListImgsDf['Total']
    rankListImgsDf = rankListImgsDf.sort_values(by = ['Proportion'],ascending = False)
    rankListImgsDf.to_csv('../data/rankListImages_expt2.csv')

    '''
    resultsAIDGIDDf > Merged data frame that add's AID info to the results data
    resultsAIDGIDDf['AID' + [resultsPerJobDf]]

    gidAidResultsFeaturesDf > A master data frame that has results data merged along with all the image features
    gidAidResultsFeaturesDf['GID','AID',[FEATURES],[resultsPerJobDf]]

    '''
    resultsAIDGIDDf = pd.merge(aidGidDf,resultsPerJobDf,left_on='GID',right_on = 'GID',how="right")

    gidAidResultsFeaturesDf = pd.merge(resultsAIDGIDDf,aidFeaturesDf,left_on = 'AID',right_on = 'AID') # most important data frame with all the info
    gidAidResultsFeaturesDf.to_csv("../data/resultsFeaturesComb_expt2.csv",index=False)


if __name__ == "__main__":
    __main__()


