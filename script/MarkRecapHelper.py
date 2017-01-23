# Mark Recapture Helper Scripts
import json
import DeriveFinalResultSet as DRS
import DataStructsHelperAPI as DS
import importlib
import pandas as pd
import warnings
import sys

importlib.reload(DS)

def genNidMarkRecapDict(inExifFl,inGidAidMapFl,inAidFtrFl,gidPropMapFl,daysDict,filterBySpecies=None,shareData='proportion',probabThreshold=1):
	with open(inExifFl,"r") as inpFl:
		jsonObj = json.load(inpFl)

	# Extract only the date information for all the given images
	# modify the date format as and when needed to match the requirements. 
	imgDateDict = {gid : DS.getDateFromStr(jsonObj[gid]['date'],'%Y-%m-%d %H:%M:%S','%Y') for gid in jsonObj.keys()}

	# filter out only the GIDs that were taken on either of the days specified in the days dictionary
	filteredGid = list(filter(lambda x : imgDateDict[x] in daysDict.keys(),imgDateDict.keys()))
	
	# Logic to handle only the images that are shared
	if shareData in {'proportion' , 'classifier' }:
		filteredGid = genSharedGids(filteredGid,gidPropMapFl,shareData,probabThreshold)
	
	# Replace the day with Mark or Recapture
	gidsDayNumFull = { gid : daysDict[imgDateDict[gid]] for gid in filteredGid } 

	# Build map of images and the individuals in it. 
	gidNid = DRS.getCountingLogic(inGidAidMapFl,inAidFtrFl,"NID",False)
	if filterBySpecies != None:
		gidSpecies = DRS.getCountingLogic(inGidAidMapFl,inAidFtrFl,"SPECIES",False)
		gidsDayNum = { gid : gidsDayNumFull[gid] for gid in gidsDayNumFull  if gid in gidSpecies.keys() and filterBySpecies in gidSpecies[gid]}
	else:
		gidsDayNum = gidsDayNumFull

	nidMarkRecap = {}
	for gid in gidsDayNum.keys(): # only iterate over the GIDs of interest
		if gid in gidNid.keys(): # not all images with valid EXIF feature will have an annotation
			for nid in gidNid[gid]:
				if int(nid) > 0 and int(nid) != 45: # ignore all the false positives --and ignore NID 45
					nidMarkRecap[nid] = nidMarkRecap.get(nid,[]) + [gidsDayNum[gid]]

	nidMarkRecapSet = { nid : list(set(nidMarkRecap[nid])) for nid in nidMarkRecap.keys()}

	return nidMarkRecapSet

# Return Petersen-Lincoln Index for mark-recapture
def applyMarkRecap(nidMarkRecapSet):
	uniqueIndsDay1 = {nid for nid in nidMarkRecapSet if 1 in nidMarkRecapSet[nid]}
	uniqueIndsDay2 = {nid for nid in nidMarkRecapSet if 2 in nidMarkRecapSet[nid]}

	marks = len(uniqueIndsDay1)
	recaptures = len(uniqueIndsDay1 & uniqueIndsDay2)
	try:
		population = len(uniqueIndsDay2) * marks / recaptures
	except:
		warnings.warn("There are no recaptures for this case.")
		population = 0

	
	return marks,recaptures,population

def genSharedGids(gidList,gidPropMapFl,shareData='proportion',probabThreshold=1):
	df = pd.DataFrame.from_csv(gidPropMapFl)

	if shareData == 'proportion':
		gidPropDict = df['Proportion'].to_dict()
		highSharedGids = { str(gid) for gid in gidPropDict.keys() if float(gidPropDict[gid]) >= 80.0 }
	else:
		gidShrDict = df['share'].to_dict()
		highSharedGids = { str(gid) for gid in gidShrDict.keys() if float(gidShrDict[gid]) >= probabThreshold }

	return list(set(gidList) & highSharedGids)

def runMarkRecap(inExifFl,inGidAidMapFl,inAidFtrFl,gidPropMapFl,daysDict,filterBySpecies=None,shareData='proportion',probabThreshold=1):
	nidMarkRecapSet = genNidMarkRecapDict(inExifFl,inGidAidMapFl,inAidFtrFl,gidPropMapFl,daysDict,filterBySpecies,shareData,probabThreshold)
	return applyMarkRecap(nidMarkRecapSet)
