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
from sklearn.metrics import classification_report,accuracy_score,f1_score,precision_score,recall_score,roc_auc_score,mean_absolute_error, mean_squared_error,zero_one_loss
import sys
import numpy as np
import ClassifierCapsuleClass as ClfClass
import importlib
importlib.reload(ClfClass)


THRESHOLD = 80
# Method for generating feature header
def genHead(dataDict,ftr):
    if ftr != 'tags':
        ftrList = [dataDict[gid][ftr].split(',') for gid in dataDict.keys()]
    else:
        ftrList = [literal_eval(dataDict[gid][ftr]) for gid in dataDict.keys()]
        
    ftrList = {item for block in ftrList for item in block}
    
    return list(ftrList)

def getMasterData(flNm):
    df = pd.DataFrame.from_csv(flNm)
    cols = list(df.columns)
    df.drop('URL',1,inplace=True)
    df.drop('Album',1,inplace=True)
    df.reset_index(inplace=True)
    df = df.iloc[np.random.permutation(len(df))]
    df.to_csv("/tmp/tmp.csv",index=False)
    
    reader = csv.reader(open("/tmp/tmp.csv","r"))
    head = reader.__next__()
    data = {}
    for row in reader:
        temp = {}
        for i in range(1,len(row)):
            temp[head[i]] = row[i] 
        data[row[0]] = temp

    return data

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
