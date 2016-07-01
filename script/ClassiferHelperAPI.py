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

THRESHOLD = 20
# Method for generating feature header
def genHead(dataDict,ftr):
    if ftr != 'tags':
        ftrList = [dataDict[gid][ftr].split(',') for gid in dataDict.keys()]
    else:
        ftrList = [literal_eval(dataDict[gid][ftr]) for gid in dataDict.keys()]
        
    ftrList = {item for block in ftrList for item in block}
    
    return list(ftrList)

def createDataFlDict(data,allAttribs,logistic=True):
    gidAttribDict = {}
    for gid in data.keys():
        ftrDict = data[gid]
        attribDict = OrderedDict.fromkeys(allAttribs,0)

        ftrs = ['SPECIES','SEX','AGE','QUALITY','VIEW_POINT']

        for ftr in ftrs:
            spcs = ftrDict[ftr].split(',')
            for itm in spcs:
                attribDict[itm] = 1

        # logic for tgs
        tgs = literal_eval(ftrDict['tags'])
        for tag in tgs:
            attribDict[tag] = 1

        if logistic:
            attribDict['TARGET'] = 1 if float(ftrDict['Proportion'] ) > 80 else 0 # Thresholding for the share proportion
        else:
            attribDict['TARGET'] = float(ftrDict['Proportion'])

        gidAttribDict[gid] = attribDict

    json.dump(gidAttribDict,open("/tmp/gidAttribDict.json","w"),indent=4)

    pd.DataFrame(gidAttribDict).transpose().to_csv("/tmp/gidAttribDict.csv")
    
    return gidAttribDict

# Accuracy of the regression model is defined as the percentage of correct predictions for LOGISTIC
# For LINEAR(MULTIPLE), its defined as the predictions that fall in the range of THRESHOLD - defined as a constant
def buildRegrModel(data,allAttribs,splitProp,overrideThreshold=THRESHOLD,logistic=True):
    THRESHOLD = overrideThreshold
    gidAttribDict = createDataFlDict(data,allAttribs,logistic)
    
    nTrain = int(len(gidAttribDict.keys()) * splitProp)
    nTest = len(gidAttribDict.keys()) - int(len(gidAttribDict.keys()) * splitProp)
    
    if logistic:
        regr = LogisticRegression()
    else:
        regr = LinearRegression()

    df = pd.DataFrame(gidAttribDict).transpose()
    df = df[allAttribs + ["TARGET"]] # Rearranging the order of the columns

    attributes = df.columns[:len(allAttribs)] # all attributes

    train_x = df[attributes].head(nTrain)
    train_y = df['TARGET'].head(nTrain)

    regr.fit(train_x,train_y)

    test_x = df[attributes].tail(nTest)
    test_y =df['TARGET'].tail(nTest) 
    test_y = list(test_y)

    predictions = regr.predict(test_x)
    predictions = list(predictions)


    count = 0
    if logistic:
        for i in range(len(predictions)):
            if predictions[i] == test_y[i]:
                count += 1
    else:        
        for i in range(len(predictions)):
            if abs(predictions[i]-test_y[i]) <= THRESHOLD: # defined as a global const, overridable 
                count += 1
    if logistic:
        return test_x, test_y, regr.predict_proba(test_x)[:,1], count*100/nTest
    else: 
        return count*100/nTest,regr # accuracy