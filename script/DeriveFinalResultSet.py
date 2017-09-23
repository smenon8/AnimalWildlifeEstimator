# coding: utf-8
# python-3
# Author: Sreejith Menon (smenon8@uic.edu)
# Creation date: 6/14/16

# Description: Contains multiple methods to calculate final result statistics. 
# The methods in this script file highly utilizes objects created by JobsMapResultsFilesToContainerObjs.py. 
# Three global variables are declared in the scope of this project, the currently point to CSV files that have information from second phase of the mechanical turk deployment. 
# gidAidMapFl, aidFeatureMapFl, imgJobMap
# These parameters are used by multiple methods within this script.

import importlib, pandas as pd, statistics as s, re, json, csv, matplotlib.pyplot as plt
import GetPropertiesAPI as GP
from collections import OrderedDict
import IBEIS_mongo_helper as IB_h
import JobsMapResultsFilesToContainerObjs as ImageMap

importlib.reload(ImageMap)
importlib.reload(GP)

# Global variables for the scope of this script
gidAidMapFl = "../data/experiment2_gid_aid_map.json"
aidFeatureMapFl = "../data/experiment2_aid_features.json"
imgJobMap = "../data/imageGID_job_map_expt2_corrected.csv"
 

def PRINT(jsonLike):
    print(json.dumps(jsonLike, indent=4))

# This method is a simplification of adding up the share/no share counts of a particular image. 
# For example, for a particular image which appeared in 5 different albums, the share rates were 9,5,9,10,10. 
# This method will return gid:sum([9,5,9,10,10]).
def genTotCnts(ovrCnts):
    dSum = {}
    for key in ovrCnts:
        dSum[key] = sum(ovrCnts[key])
        
    return dSum

# This dictionary answers the question, what percentage of this feature/image were shared. 
# The share proportion is calculated as total_shares/(total_shares+total_not_shares).
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
# This method defines the counting logic for a particular image for a given feature. 
# For instance, for the feature ‘SPECIES’, there might be images that contains both a zebra and a giraffe. 
# In that case, the share counts have to be added to both zebra and giraffe.
def getCountingLogic(*args, **kwargs):
    if len(kwargs.keys()):
        client, feature, source, withNumInds = args[0], args[1], args[2], args[3]
        featuresPerImg = IB_h.extractImageFeaturesFromMap(client, feature, source=source)
    else:
        gidAidMapFl, aidFeatureMapFl, feature, withNumInds = args[0], args[1], args[2], args[3]
        if len(args) == 5:
            mode = args[4]
        else:
            mode = "GZC"
        featuresPerImg = ImageMap.extractImageFeaturesFromMap(gidAidMapFl, aidFeatureMapFl, feature, mode=mode)

    countLogic = {}
    for gid in featuresPerImg.keys():
        numInds = len(featuresPerImg[gid])  # number of individuals in a particular image
        countFor = list(set(featuresPerImg[gid]))
        if withNumInds:
            countLogic[gid] = [numInds, countFor]
        else:
            countLogic[gid] = countFor

    return countLogic

def getCountingLogic_old(gidAidMapFl,aidFeatureMapFl,feature,withNumInds=True, mode="GZC"):
    featuresPerImg = ImageMap.extractImageFeaturesFromMap(gidAidMapFl,aidFeatureMapFl,feature, mode=mode)
    
    countLogic = {}
    for gid in featuresPerImg.keys():
        numInds = len(featuresPerImg[gid]) # number of individuals in a particular image
        countFor = list(set(featuresPerImg[gid]))
        if withNumInds:
            countLogic[gid] = [numInds,countFor]
        else:
            countLogic[gid] = countFor
        
    return countLogic

# This method is used to generate the number of shares and not_shares per feature in a particular album. 
# For instance, if the required features list contains ‘SPECIES’, then it tells the share and not_share count per album for each available/identifiable species.
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

# This method derives the share proportions of images across different albums as opposed to generating an overall proportion of images. 
# For example, the output of this method will contain how many times a particular image was shared in a particular album. 
# This is particularly insightful for images that appear across multiple albums. 
# It could essentially tell if a certain image was shared in the same way or differently and if the share rate of an image is orthogonal to the context of album.
def getShrPropImgsAcrossAlbms(imgJobMap,resSetStrt,resSetEnd,flNm):
    imgAlbumDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)
    master = ImageMap.createResultDict(resSetStrt,resSetEnd)
    imgShareNotShareList,noResponse = ImageMap.imgShareCountsPerAlbum(imgAlbumDict,master)

    albumGidDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)

    # filters the GID's that appears in multiple albums
    imgsInMultAlbms = list(filter(lambda x : len(albumGidDict[x]) > 1,albumGidDict.keys()))

    gidAlbmDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)

    imgAlbmPropDict = {} # image album proportion dict
    for tup in imgShareNotShareList:
        if tup[0] in imgsInMultAlbms:
            imgAlbmPropDict[(tup[0],tup[1])] = tup[4]

    return imgAlbmPropDict,getConsistencyDict(imgsInMultAlbms,gidAlbmDict,imgAlbmPropDict,flNm)

# This method returns a lambda function or a logic in filtering all valid rows without the UNIDENTIFIED. 
# A slight adjustment is needed depending on what feature is being filtered.
def getFltrCondn(ftr):
    if ftr=='NID':
        return lambda x : x[0] != 'UNIDENTIFIED' and int(x[0]) > 0
    else: # for all other features
        return lambda x : x[0] != 'UNIDENTIFIED' 

# This is a helper method for getConsistencyDict(). It returns three objects.
# i. A list with only valid features i.e. without the UNIDENTIFIED entries. 
# ii. A dictionary object that contains the albums in which a particular feature is seen. Ex. GIRAFFE is seen in albums 1, 3,4,5 etc. 
# iii. A dictionary object that contains the share proportion of feature per album. Ex. giraffes in album 1 were shared 70% of times etc. Format of the key: (feature, album)
def genObjsForConsistency(gidAidMapFl,aidFeatureMapFl,ftr,imgJobMap,resSetStrt=1,resSetEnd=100):    
    d = shrCntsByFtrPrAlbm(gidAidMapFl,aidFeatureMapFl,ftr,imgJobMap,resSetStrt,resSetEnd)

    fltrCondn = getFltrCondn(ftr)
    d_filtered = {}
    d_filtered_keys = list(filter(fltrCondn, d.keys()))
    for key in d_filtered_keys:
        d_filtered[key] = d[key]

    ftrAlbmPropDict = getShrProp(d_filtered)
    filteredKeyArr = [x[0] for x in ftrAlbmPropDict.keys()]

    ftrAlbmDict = {}
    for ftr,albm in ftrAlbmPropDict.keys():
        ftrAlbmDict[ftr] = ftrAlbmDict.get(ftr,[]) + [albm]
        
    return filteredKeyArr,ftrAlbmDict,ftrAlbmPropDict

# This method should be thought as the main counting logic while calculating the share rate related statistic for any feature that is extracted from IBEIS. 
# The output dictionary is all the valid features and thier share-rates across different albums. 
# The output dictionary is a key - dictionary pair. Ex. {giraffe : {album_1 : 70, album_2 : 89}, ...}
def getConsistencyDict(filteredKeyArr,ftrAlbmDict,ftrAlbmShrPropDict,flNm='/tmp/getConsistencyDict.output'):
    consistency = {}
    for ftr in filteredKeyArr:
        tempDict = {}
        for albm in ftrAlbmDict[ftr]:
            tempDict[albm] = ftrAlbmShrPropDict.get((ftr,albm),None)
        consistency[ftr] = tempDict

    consistency_mult = {}
    for key in consistency:
        if len(consistency[key]) > 1:
            consistency_mult[key] = consistency[key]

    fl = open(flNm,"w")
    json.dump(consistency_mult,fl,indent=4)
    fl.close()
        
    return consistency_mult

# consistency object is retuned by getShrPropImgsAcrossAlbms()
# his method generates the mean, variance and standard deviation for a particular feature element for across different albums. 
def genVarStddevShrPropAcrsAlbms(consistency):    
    gidShrVarStdDevDict = {}
    for gid in consistency:
        albmShrRateD = consistency[gid]

        if None not in albmShrRateD.values():
            var = s.variance(albmShrRateD.values())
            mean = s.mean(albmShrRateD.values())
            std = s.stdev(albmShrRateD.values())

            gidShrVarStdDevDict[gid] = {'mean' : mean,
                                        'variance' : var,
                                       'standard_deviation' : std}

    return gidShrVarStdDevDict

# This method generates the overall share statistic for every element of a particular feature. 
# The logic involves simple counting for each element of the feature based on the counting logic. 
# This explicitly handles the images where there are multiple features and the counts are made in each of the feature. 
# This method is ideal for getting share rate of a particular feature across the entire experiment, not limited by album. 
# In other words, the result dict has share proportions calculated across albums. 
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

# This method generates the share statistic for every element of a particular feature for each album in which there are some instances with the said feature. 
# The logic involves simple counting for each element of the feature based on the counting logic. 
# This explicitly handles the images where there are multiple features and the counts are made in each of the feature. 
# This method is ideal for getting share rate of a particular feature across the entire experiment by album. 
# In other words, this should used to calculate and compare the share rates of a particular feature and how it changes across different albums. 
# As a sidenote, if the same feature is being shared differently across albums, then it means there is some contextual information from the album that is dominating this effect.
def shrCntsByFtrPrAlbm(gidAidMapFl,aidFeatureMapFl,feature,imgJobMap,resSetStrt=1,resSetEnd=100):
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

# This method is used to generate cross statistic for two features. 
# The logic involves simple counting for each element of the feature based on the counting logic. 
# Since there are two features to be dealt here, the instances are divided into even and uneven features. 
# Even features are defined as when the number of instances of feature 1 and feature 2 are identical. 
# Uneven features on the other hand are when the number of instances of feature 1 and feature 2 are not identical. 
# Uneven features are handled differently for 1-many, many-1 and many-many.
def ovrallShrCntsByTwoFtrs(getCountingLogicgidAidMapFl,aidFeatureMapFl,ftr1,ftr2,imgJobMap,resSetStrt,resSetEnd):
    countLogic1 = (gidAidMapFl,aidFeatureMapFl,ftr1)
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
          
    # handling un-even features - issues after GetPropertiesAPI update - issue being tracked - issue name: Issue with consolidated feature file #1
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

# This method generates the rank list of number of individuals in an image by share proportion.
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

# Comments:  Number of shares/not shares for each and every position are enumerated inside a list. 
# Use of OrderedDict() from the Python collections framework ensures that the records are picked in the exact same order they appear in the albums. 
# This returned dictionary can then be embedded inside a data-frame and can be visualized.
def getPosShrProptn(imgJobMap,resStart,resEnd):    
    pos = {} # 1:(shr,noShr,prop)
    for i in range(resStart,resEnd):
        results = ImageMap.createResultDict(i,i)
        imgAlbumDict = ImageMap.genImgAlbumDictFromMap(imgJobMap)
        shrCnt,junk = ImageMap.imgShareCountsPerAlbum(imgAlbumDict,results)

        for i in range(1,len(shrCnt)+1):
            pos[i] = pos.get(i,[]) + [(shrCnt[i-1][2],shrCnt[i-1][3])]

    summaryPosCnt = OrderedDict()
    for position in pos:
        shrs = [x[0] for x in pos[position]]
        notShrs = [x[1] for x in pos[position]]

        total = [x[0]+x[1] for x in pos[position]]

        summaryPosCnt[position] = {'share' : sum(shrs),
                                  'not_share' : sum(notShrs),
                                  'total': sum(total)
                                  }

    for pos in summaryPosCnt:
        dct = summaryPosCnt[pos]
        dct['proportion'] = dct['share'] * 100 / dct['total']  

    return summaryPosCnt

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
    #rankListImgsDf.to_csv('../FinalResults/rankListImages_expt2.csv')

    '''
    resultsAIDGIDDf > Merged data frame that add's AID info to the results data
    resultsAIDGIDDf['AID' + [resultsPerJobDf]]

    gidAidResultsFeaturesDf > A master data frame that has results data merged along with all the image features
    gidAidResultsFeaturesDf['GID','AID',[FEATURES],[resultsPerJobDf]]

    '''
    resultsAIDGIDDf = pd.merge(aidGidDf,resultsPerJobDf,left_on='GID',right_on = 'GID',how="right")

    gidAidResultsFeaturesDf = pd.merge(resultsAIDGIDDf,aidFeaturesDf,left_on = 'AID',right_on = 'AID') # most important data frame with all the info
    gidAidResultsFeaturesDf.to_csv("../FinalResults/resultsFeaturesComb_expt2.csv",index=False)


if __name__ == "__main__":
    __main__()


