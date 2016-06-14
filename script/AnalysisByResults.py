# Generate Final Analysis files
import importlib
import JobsMapResultsFilesToContainerObjs as ImageMap
import pandas as pd
importlib.reload(ImageMap)
'''
Snippet for generating the imgShareNotShareList from the results file obtained from mechanical turk 
Range specified 
noResponse has all those images that do not have any response from the HTMLQuestion
resultsPerJobDf['GID','Album','Shared','Not Shared','Proportion']
'''
imgAlbumDict = ImageMap.genImgAlbumDictFromMap("../data/imageGID_job_map_expt2_corrected.csv")
master = ImageMap.createResultDict(1,10)
imgShareNotShareList,noResponse = ImageMap.imgShareCountsPerAlbum(imgAlbumDict,master)

resultsPerJobDf = pd.DataFrame(imgShareNotShareList,columns = ['GID','Album','Shared','Not Shared','Proportion'])

'''****************************************************************************************************************'''

'''
Code for reading from json files into data frames
aidGidDf['AID','GID']
aidFeaturesDf['AID',[FEATURES]]
'''
aidGidDict = ImageMap.genAidGidTupListFromMap('../data/experiment2_gid_aid_map.json')
aidGidDf= pd.DataFrame(aidGidDict,columns = ['AID','GID'])

aidFeaturesDf = pd.DataFrame(ImageMap.genAidFeatureDictList('../data/experiment2_aid_features.json'))
aidFeaturesDf['AID'] = aidFeaturesDf['AID'].astype('int32')

'''****************************************************************************************************************'''

# Aggregated Data Frames
aggResultsGIDDf = resultsPerJobDf.groupby(['GID'])['Shared','Not Shared'].sum() # > Gives you the results of number of times each image was shared across the whole expt
aggResultsGIDDf['Proportion'] = aggResultsGIDDf['Shared'] * 100 / (aggResultsGIDDf['Shared'] +aggResultsGIDDf['Not Shared'])

mergedResultsAIDGIDCombDf = pd.merge(aidGidDf,resultsPerJobDf,left_on='GID',right_on = 'GID') # > Gives you the aggregated data frame with no. of shares per annotation ID (album wise)

# not needed / no particularly insightful data
aggResultsAIDDf = mergedResultsAIDGIDCombDf.groupby(['AID'])['Shared','Not Shared'].sum() # > Gives you the results of number of times each annotation was shared across the whole expt
aggResultsAIDDf['Proportion'] = aggResultsAIDDf['Shared'] * 100 / (aggResultsAIDDf['Shared'] + aggResultsAIDDf['Not Shared'])


gidResultsFeaturesCombDf = pd.merge(mergedResultsAIDGIDCombDf,aidFeaturesDf,left_on = 'AID',right_on = 'AID') # most important data frame with all the info
gidResultsFeaturesCombDf.to_csv("../data/resultsFeaturesComb.csv")

shareRateBySpecies = gidResultsFeaturesCombDf[['GID','SPECIES','Shared','Not Shared']]

shareRateBySpecies = shareRateBySpecies.drop_duplicates(subset='GID', keep = 'last')
shareRateBySpecies = shareRateBySpecies.groupby(['SPECIES'])['Shared','Not Shared'].sum()
shareRateBySpecies['Proportion'] = shareRateBySpecies['Shared'] * 100 / (shareRateBySpecies['Shared'] + shareRateBySpecies['Not Shared'])


aggIndividualsDf = gidResultsFeaturesCombDf.groupby(['INDIVIDUAL_NAME'])['Shared','Not Shared'].sum()
aggIndividualsDf['Proportion'] = aggIndividualsDf['Shared'] * 100 / (aggIndividualsDf['Shared'] + aggIndividualsDf['Not Shared'])


grouped = gidResultsFeaturesCombDf.groupby(['GID'])
grouped = grouped.aggregate(lambda x: tuple(x))[['SPECIES']]
grouped['SPECIES'].tolist()

print(aggResultsGIDDf.head())
print()
print(aggResultsAIDDf.head())