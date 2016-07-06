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

THRESHOLD = 80
# Method for generating feature header
def genHead(dataDict,ftr):
    if ftr != 'tags':
        ftrList = [dataDict[gid][ftr].split(',') for gid in dataDict.keys()]
    else:
        ftrList = [literal_eval(dataDict[gid][ftr]) for gid in dataDict.keys()]
        
    ftrList = {item for block in ftrList for item in block}
    
    return list(ftrList)

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
            spcs = ftrDict[ftr].split(',')
            for itm in spcs:
                attribDict[itm] = 1

        # logic for tgs
        tgs = literal_eval(ftrDict['tags'])
        for tag in tgs:
            attribDict[tag] = 1

        if binaryClf:
            attribDict['TARGET'] = 1 if float(ftrDict['Proportion'] ) > threshold else 0 # Thresholding for the share proportion
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
            raise Exception('Exception : Classifier Method Unknown')
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


# returns test attributes, actual test TARGET, predicted values and predicition probabilities
def buildBinClassifier(data,allAttribs,trainTestSplit,threshold,methodName,extremeClf=True):
    gidAttribDict = createDataFlDict(data,allAttribs,True,threshold,extremeClf) # binaryClf attribute in createDataFlDict will be True here

    train_x,test_x,train_y,test_y = trainTestSplitter(gidAttribDict,allAttribs,trainTestSplit) # new statement
    clf = getClassifierAlgo(methodName)
    clf.fit(train_x,train_y)

    predictions = list(clf.predict(test_x))

    return clf,test_x,test_y,predictions,clf.predict_proba(test_x)[:,1],clf.score(test_x,test_y) # prediction probabilities

