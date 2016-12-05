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
from sklearn.linear_model import LogisticRegression, LinearRegression, Lasso, Ridge, ElasticNet
from sklearn import svm,tree,naive_bayes
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.dummy import DummyClassifier
import sys
import numpy as np
import ClassifierCapsuleClass as ClfClass
import importlib
import RegressionCapsuleClass as RgrClass
importlib.reload(ClfClass)
importlib.reload(RgrClass)


THRESHOLD = 80

# Method for generating feature header
# Converting the categorical features into dummy variables
# Returns a list of list
def genHead(dataDict, ftr):
    if ftr != 'tags':
        ftrList = [dataDict[gid][ftr].split(',') for gid in dataDict.keys()]
    else:
        ftrList = [literal_eval(dataDict[gid][ftr]) for gid in dataDict.keys()]
        
    ftrList = {item for block in ftrList for item in block}
    
    return list(ftrList)


def getMasterData(flNm):
    df = pd.DataFrame.from_csv(flNm)

    df.reset_index(inplace=True)
    df = df.iloc[np.random.permutation(len(df))]
    df['GID'] = df['GID'].astype(str)

    df.index = df['GID']
    if 'URL' in df.columns: 
        df.drop(['GID','URL','Album'],1,inplace=True)
    else:
        df.drop(['GID'],1,inplace=True)

    return df.to_dict(orient='index')

# Flatten out the list of lists p
def genAttribsHead(data, ftrList):
    return [attrib for ftr in ftrList for attrib in genHead(data,ftr)]

# Filling in 0's and 1's for the dummy variables.
def createDataFlDict(data, allAttribs, threshold, dataMode ='Train', writeTempFiles=False, ftrs = ['SPECIES','SEX','AGE','QUALITY','VIEW_POINT','INDIVIDUAL_NAME']):
    gidAttribDict = {}

    if dataMode == 'Train':
        fDataKeys= list(filter(lambda x : float(data[x]['Proportion']) >= 80.0 or float(data[x]['Proportion']) <= 20.0,data.keys()))
        fData = {gid: data[gid] for gid in fDataKeys}
    else: # there will be no proportion, unlablelled data
        fData = data

    for gid in fData.keys():
        ftrDict = fData[gid]
        attribDict = OrderedDict.fromkeys(allAttribs,0)

        for ftr in ftrs:
            for itm in set(ftrDict[ftr].split(',')):
                if itm in allAttribs:
                    attribDict[itm] = 1

        # logic for tgs
        for tag in set(literal_eval(ftrDict['tags'])):
            if tag in allAttribs:
                attribDict[tag] = 1

        if dataMode == 'Train':
            attribDict['TARGET'] = 1 if float(ftrDict['Proportion'] ) >= threshold else 0 # Thresholding for the share proportion

        gidAttribDict[gid] = attribDict
    
    if writeTempFiles:
        json.dump(gidAttribDict,open("/tmp/gidAttribDict.json","w"),indent=4)
        pd.DataFrame(gidAttribDict).transpose().to_csv("/tmp/gidAttribDict.csv")
        
    return gidAttribDict


def getLearningAlgo(methodName, kwargs):
    if methodName == 'logistic':
        return LogisticRegression(**kwargs)
    elif methodName == 'svm':
        return svm.SVC(**kwargs)
    elif methodName == 'linear_svr':
        return svm.LinearSVR(**kwargs)
    elif methodName == 'svr':
        return svm.SVR()
    elif methodName == 'dtree':
        return tree.DecisionTreeClassifier(**kwargs)
    elif methodName == 'dtree_regressor':
        return tree.DecisionTreeRegressor()
    elif methodName == 'random_forests':
        return RandomForestClassifier(**kwargs)
    elif methodName == 'bayesian':
        return naive_bayes.BernoulliNB(**kwargs)
    elif methodName == 'ada_boost':
        return AdaBoostClassifier(**kwargs)
    elif methodName == 'dummy':
        return DummyClassifier(**kwargs)
    elif methodName == 'linear':
        return LinearRegression(**kwargs)
    elif methodName == 'ridge':
        return Ridge(**kwargs)
    elif methodName == 'lasso':
        return Lasso(**kwargs)
    else:
        try:
            raise Exception('Exception : Classifier Method %s Unknown' %methodName)
        except Exception as inst:
            print(inst.args)
            sys.exit()

def trainTestSplitter(gidAttribDict, allAttribs, trainTestSplit):
    df = pd.DataFrame(gidAttribDict).transpose()
    df = df[allAttribs + ["TARGET"]] # Rearranging the order of the columns

    targetVar = df['TARGET']
    del df['TARGET']    
    return train_test_split(df, targetVar, test_size=trainTestSplit,random_state=0)

# Returns a classifier object of Type ClassifierCapsuleClass
def buildBinClassifier(data, allAttribs, trainTestSplit, threshold, methodName, kwargs=None):
    gidAttribDict = createDataFlDict(data,allAttribs,threshold) # binaryClf attribute in createDataFlDict will be True here

    train_x, test_x, train_y, test_y = trainTestSplitter(gidAttribDict, allAttribs, trainTestSplit) # new statement
    clf = getLearningAlgo(methodName,kwargs)
    
    clfObj = ClfClass.ClassifierCapsule(clf,methodName,trainTestSplit,train_x,train_y,test_x,test_y)

    return clfObj


# Generating attributes, converting categorical attributes into discrete binary output.
# For instance - SPECIES : Zebra will be converted into (Zebra: 1, Giraffe: 0 .. )
def genAllAttribs(masterDataFl, constraint, infoGainFlNm=None):
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


def buildRegrMod(train_data_fl, allAttribs, trainTestSplit, methodName, kwargs=None):
    train_data= getMasterData(train_data_fl)
    gidAttribDict = createDataFlDict(train_data,allAttribs,80,dataMode='regression')

    df = pd.DataFrame(gidAttribDict).transpose()
    dfCol = df.columns
    df.reset_index(inplace=True)
    df.columns = ['GID'] + list(dfCol)
    df['GID'] = df['GID'].apply(pd.to_numeric)

    dfResults = pd.DataFrame.from_csv(train_data_fl)['Proportion'].reset_index()
    regressionData = pd.merge(df,dfResults,on='GID')
    regressionData.drop(['GID'],1,inplace=True)

    rgr = getLearningAlgo(methodName,kwargs)
    ftrs = list(regressionData.columns)
    ftrs.remove('Proportion')

    X = regressionData[ftrs]
    y = regressionData['Proportion']
    if trainTestSplit != 0:
        train_x,test_x,train_y,test_y = train_test_split(X,y,test_size=1-trainTestSplit,random_state=0)
    else:
        train_x,test_x,train_y,test_y = X, None, y, None

    rgrObj = RgrClass.RegressionCapsule(rgr,methodName,trainTestSplit,train_x,train_y,test_x,test_y)

    return rgrObj


