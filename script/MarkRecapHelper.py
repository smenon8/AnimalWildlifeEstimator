# Mark Recapture Helper Scripts
import json
import DeriveFinalResultSet as DRS
import DataStructsHelperAPI as DS
import importlib

importlib.reload(DS)

def genNidMarkRecapDict(inExifFl,inGidAidMapFl,inAidFtrFl,daysDict,filterBySpecies=None):
	with open(inExifFl,"r") as inpFl:
		jsonObj = json.load(inpFl)

	# Extract only the date information for all the given images
	imgDateDict = {gid : DS.getDateFromStr(jsonObj[gid]['datetime'],'%Y-%m-%d %H:%M:%S','%Y-%m-%d') for gid in jsonObj.keys()}

	# filter out only the GIDs that were taken on either of the days specified in the days dictionary
	filteredGid = list(filter(lambda x : imgDateDict[x] in daysDict.keys(),imgDateDict.keys()))

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
				if int(nid) > 0: # ignore all the false positives
					nidMarkRecap[nid] = nidMarkRecap.get(nid,[]) + [gidsDayNum[gid]]

	nidMarkRecapSet = { nid : list(set(nidMarkRecap[nid])) for nid in nidMarkRecap.keys()}

	return nidMarkRecapSet

def applyMarkRecap(nidMarkRecapSet):
	uniqueIndsDay1 = {nid for nid in nidMarkRecapSet if 1 in nidMarkRecapSet[nid]}
	uniqueIndsDay2 = {nid for nid in nidMarkRecapSet if 2 in nidMarkRecapSet[nid]}

	marks = len(uniqueIndsDay1)
	recaptures = len(uniqueIndsDay1 & uniqueIndsDay2)
	population = len(uniqueIndsDay2) * marks / recaptures
	
	return population