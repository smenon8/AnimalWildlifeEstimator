# Mark Recapture Helper Scripts
import json
import DeriveFinalResultSet as DRS
import DataStructsHelperAPI as DS
import importlib
import pandas as pd
import warnings
import sys, math
importlib.reload(DS)
MODE = 'GGR'
'''

add logic to handle zoo animals in a different function
handle_zoo_animals(bottom_left_lat, bottom_left_long, top_right_lat, top_right_long)
should return animals that are found within this rectangular area in the map
Issue #15
'''

def gid_filter_logic(inExifFl, inGidAidMapFl, inAidFtrFl):
	with open(inExifFl,"r") as inpFl:
		jsonObj = json.load(inpFl)

	# to preserve only images taken in wild - should be commented when not needed.
	gids_nairobi = [gid for gid in jsonObj.keys() if jsonObj[gid]['lat'] >= -1.50278 and jsonObj[gid]['lat'] <= 1.504953 and jsonObj[gid]['long'] >= 35.174045 and jsonObj[gid]['long'] <= 38.192836 ]
	gids_geo_tagged = [gid for gid in jsonObj.keys() if jsonObj[gid]['lat'] != 0 or jsonObj[gid]['long'] != 0]
	gids_zoo = list(set(gids_geo_tagged) - set(gids_nairobi))

	gid_nid = DRS.getCountingLogic(inGidAidMapFl,inAidFtrFl,"NID",False)
	nid_gid = DS.flipKeyValue(gid_nid)

	nids_zoo = []
	for gid in gid_nid.keys():
		if gid in gids_zoo:
			nids_zoo.extend(gid_nid[gid]) # this will take care of list of lists

	nids_in_wild_gid_map = {nid: nid_gid[nid] for nid in nid_gid.keys() if nid not in nids_zoo}

	# this contains all the images that have no animals that were even once identified in the zoo
	gid_list = list({gid for sublist in list(nids_in_wild_gid_map.values()) for gid in sublist})

	return gid_list

def genNidMarkRecapDict(inExifFl,inGidAidMapFl,inAidFtrFl,gidPropMapFl,daysDict,filterBySpecies=None,shareData='proportion',probabThreshold=1):
	with open(inExifFl,"r") as inpFl:
		jsonObj = json.load(inpFl)

	# Extract only the date information for all the given images
	# modify the date format as and when needed to match the requirements. 

	## for calculating year-wise mark recapture estimates
	# imgDateDict = {gid : DS.getDateFromStr(jsonObj[gid]['date'],'%Y-%m-%d %H:%M:%S','%Y') for gid in jsonObj.keys()} 

	## for calculating regular mark-recapture estimate
	imgDateDict = {gid : DS.getDateFromStr(jsonObj[gid]['datetime'],'%Y-%m-%d %H:%M:%S','%Y-%m-%d') for gid in jsonObj.keys()} 


	# gid_list = gid_filter_logic(inExifFl, inGidAidMapFl, inAidFtrFl) # -- not needed always

	# filter out only the GIDs that were taken on either of the days specified in the days dictionary
	filteredGid = list(filter(lambda x : imgDateDict[x] in daysDict.keys(),imgDateDict.keys()))
	# filteredGid = [gid for gid in filteredGid if gid in gid_list] # should be commented once done -- not needed always

	# Logic to handle only the images that are shared
	if shareData in {'proportion' , 'classifier' }:
		filteredGid = genSharedGids(filteredGid,gidPropMapFl,shareData,probabThreshold)
	
	# Replace the day with Mark or Recapture
	gidsDayNumFull = { gid : daysDict[imgDateDict[gid]] for gid in filteredGid } 

	# Build map of images and the individuals in it. 
	gidNid = DRS.getCountingLogic(inGidAidMapFl,inAidFtrFl,"NID",False, MODE)
	if filterBySpecies != None:
		gidSpecies = DRS.getCountingLogic(inGidAidMapFl,inAidFtrFl,"SPECIES",False, MODE)
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
	day2_sights = len(uniqueIndsDay2)
	try:
		population =  day2_sights * marks / recaptures
		confidence = 1.96 * math.sqrt(marks**2 * day2_sights * (day2_sights-recaptures) / recaptures**2)
	except:
		warnings.warn("There are no recaptures for this case.")
		population = 0
		confidence=0
		print(recaptures)

	
	return marks,recaptures,population,confidence

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
