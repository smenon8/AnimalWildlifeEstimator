# python3
'''
Creation date: 06/30/2016
Author : Sreejith Menon (smenon8@uic.edu)
'''
# Methods for building regression models for tagged data
import csv
from ast import literal_eval
import pandas as pd
import json
from collections import OrderedDict
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import svm,tree
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
import sys
import numpy as np
import ClassifierCapsuleClass as ClfClass
import importlib
importlib.reload(ClfClass)


THRESHOLD = 80

# Method for generating feature header
# Converting the categorical features into dummy variables
# Returns a list of list
def genHead(dataDict,ftr):
    if ftr != 'tags':
        ftrList = [dataDict[gid][ftr].split(',') for gid in dataDict.keys()]
    else:
        ftrList = [literal_eval(dataDict[gid][ftr]) for gid in dataDict.keys()]
        
    ftrList = {item for block in ftrList for item in block}
    
    return list(ftrList)

# Filling in 0's and 1's for the dummy variables.
def getMasterData(flNm):
    df = pd.DataFrame.from_csv(flNm)
    cols = list(df.columns)
    df.drop('URL',1,inplace=True)
    df.drop('Album',1,inplace=True)
    df.reset_index(inplace=True)
    df = df.iloc[np.random.permutation(len(df))]
    df.to_csv("/tmp/tmp.csv",index=False)
    
    with open("/tmp/tmp.csv","r") as tmpFL:
        reader = csv.reader(tmpFL)
        head = reader.__next__()
        data = {}
        for row in reader:
            temp = {}
            for i in range(1,len(row)):
                temp[head[i]] = row[i] 
            data[row[0]] = temp

    return data

# Flatten out the list of lists p
def genAttribsHead(data,ftrList):
    return [attrib for ftr in ftrList for attrib in genHead(data,ftr)]


def createDataFlDict(data,allAttribs,binaryClf,threshold,extremeClf = False):
    gidAttribDict = {}

    if extremeClf:
        fDataKeys= list(filter(lambda x : float(data[x]['Proportion']) >= 80.0 or float(data[x]['Proportion']) <= 20.0,data.keys()))
        fData = {gid: data[gid] for gid in fDataKeys}
    else:
        fData = data

    for gid in fData.keys():
        ftrDict = fData[gid]
        attribDict = OrderedDict.fromkeys(allAttribs,0)

        ftrs = ['SPECIES','SEX','AGE','QUALITY','VIEW_POINT','INDIVIDUAL_NAME']

        for ftr in ftrs:
            for itm in ftrDict[ftr].split(','):
                attribDict[itm] = 1

        # logic for tgs
        for tag in literal_eval(ftrDict['tags']):
            attribDict[tag] = 1

        if binaryClf:
            attribDict['TARGET'] = 1 if float(ftrDict['Proportion'] ) >= threshold else 0 # Thresholding for the share proportion
        else:
            attribDict['TARGET'] = float(ftrDict['Proportion'])

        gidAttribDict[gid] = attribDict

    json.dump(gidAttribDict,open("/tmp/gidAttribDict.json","w"),indent=4)

    pd.DataFrame(gidAttribDict).transpose().to_csv("/tmp/gidAttribDict.csv")
    
    return gidAttribDict


def getClassifierAlgo(methodName):
    if methodName == 'logistic':
        return LogisticRegression()
    elif methodName == 'svm':
        return svm.SVC(probability=True)
    elif methodName == 'dtree':
        return tree.DecisionTreeClassifier()
    elif methodName == 'random_forests':
        return RandomForestClassifier()
    else:
        try:
            raise Exception('Exception : Classifier Method %s Unknown' %methodName)
        except Exception as inst:
            print(inst.args)
            sys.exit()

def trainTestSplitter(gidAttribDict,allAttribs,trainTestSplit):
    df = pd.DataFrame(gidAttribDict).transpose()
    df = df[allAttribs + ["TARGET"]] # Rearranging the order of the columns

    attributes = df.columns[:len(allAttribs)] # all attributes

    dataFeatures = df[attributes]
    targetVar = df['TARGET']
    
    return train_test_split(dataFeatures, targetVar, test_size=trainTestSplit,random_state=0)

# Returns a classifier object of Type ClassifierCapsuleClass
def buildBinClassifier(data,allAttribs,trainTestSplit,threshold,methodName,extremeClf=True):
    gidAttribDict = createDataFlDict(data,allAttribs,True,threshold,extremeClf) # binaryClf attribute in createDataFlDict will be True here

    train_x,test_x,train_y,test_y = trainTestSplitter(gidAttribDict,allAttribs,trainTestSplit) # new statement
    clf = getClassifierAlgo(methodName)
    clfObj = ClfClass.ClassifierCapsule(clf,methodName,trainTestSplit,train_x,train_y,test_x,test_y)

    return clfObj


# Generating attributes, converting categorical attributes into discrete binary output.
# For instance - SPECIES : Zebra will be converted into (Zebra: 1, Giraffe: 0 .. )
def genAllAttribs(masterDataFl,constraint,infoGainFlNm=None):
    data = getMasterData(masterDataFl)
    if constraint == "sparse":
        ftrList = ['SPECIES','SEX','AGE','QUALITY','VIEW_POINT','INDIVIDUAL_NAME','CONTRIBUTOR','tags'] 
        allAttribs = genAttribsHead(data,ftrList)
    elif constraint == "non_sparse":
        ftrList = ['SPECIES','SEX','AGE','QUALITY','VIEW_POINT', 'tags']
        allAttribs = genAttribsHead(data,ftrList)
    elif constraint == "non_zero":
        with open(infoGainFlNm,"r") as infoGainFlNm:
            allAttribs = [row[0] for row in csv.reader(infoGainFlNm) if float(row[1]) != 0]
    elif constraint == "abv_mean":
        with open(infoGainFlNm,"r") as infoGainFlNm:
            infoGains = [(row[0],float(row[1])) for row in csv.reader(infoGainFlNm)]
        infoGainNums = [row[1] for row in infoGains]
        avg = np.mean(infoGainNums)
        allAttribs = [row[0] for row in infoGains if float(row[1]) >= avg]
    
    return allAttribs
