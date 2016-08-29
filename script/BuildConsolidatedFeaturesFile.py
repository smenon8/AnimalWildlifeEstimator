# python-3
# coding: utf-8
'''
Script Name: BuildConsolidatedFeaturesFile.py

Created date : Sunday, 27th March

Author : Sreejith Menon

Description : 
buildFeatureFl(input file,output file)
Reads from a csv file (taken as a parameter) containing a list of image GIDs. 

Extracts the below features from the IBEIS dataset:
1. nid
2. names
3. species_texts
4. sex_texts
5. age_months_est
6. exemplar_flags
7. quality_texts

Outputs 3 files in the same directory as the outFL directory
File 1 : Map of all images and their annotation IDs (csv)
File 2 : Annotation ID's and their features (csv)
File 3 : Image GID, annotation ID's and their features (csv)
File 4 : Image GID, annotation ID's and their features (json)
'''

import csv
import GetPropertiesAPI as GP
import importlib
import json
#importlib.reload(GP) # un-comment if there are any changes made to API
import sys
import math

def printCompltnPercent(percentComplete):
	i = int(percentComplete)
	sys.stdout.write('\r')
    # the exact output you're looking for:
	sys.stdout.write("[%-100s] %d%%" % ('='*i, i))
	sys.stdout.flush()

def writeCsvFromDict(header,inDict,outFL):
	writeFL = open(outFL,'w')
	writer = csv.writer(writeFL)
	writer.writerow(header)

	for key in inDict.keys():
		if inDict[key] == None:
			value = ["NONE"]
		else:
			value = inDict[key]
			writer.writerow([key] + value)
	
	writeFL.close()

def buildExifFeatureFl(inp,outFL,isInpFl = True):
	if isInpFl:
		with open(inp,"r") as inpFL:
			gids = [row[0] for row in csv.reader(inpFL)]
	else: #input is provided as a list
		gids = inp 

	gids = list(map(lambda x : int(x),gids))
	datetimes = GP.getExifData(gids,'unixtime')
	lats = GP.getExifData(gids,'lat')
	longs = GP.getExifData(gids,'lon')

	imgProps = {gids[i] : {'datetime' : GP.getUnixTimeReadableFmt(datetimes[i]),
                      'lat' : lats[i],
                      'long' : longs[i]} 
           for i in range(0,len(gids))}

	with open(outFL,"w") as outFl:
	    json.dump(imgProps,outFl,indent=4)

	return None

# Original Microsoft Tagging API output is a R list, 
# This method parses the data into python readable form and dumps the output into a JSON.
def genJsonFromMSAIData(flName,outFlNm):
    data = []
    with open(flName) as openFl:
        for row in openFl:
            data.append(row)


    cleanData = []
    for row in data:
        cleanData.append(row.replace("\\","").replace('"\n',""))

    apiResultsDict = {}

    for i in range(1,len(cleanData)):
        key,value = cleanData[i].split("\t")
        value = value.replace('"{"tags"','{"tags"')
        key = key.replace('"','')
        apiResultsDict[key] = json.loads(value)

    json.dump(apiResultsDict,open(outFlNm,"w"),indent=4)
    
    return None

# Logic for reading data from the consolidatedHITResults file - changed
# The input for the below method will be a csv file/list with all the image GID's for which the features have to be extracted.
def buildFeatureFl(inp,outFL,isInpFl = True):
	allGID = []

	if isInpFl:
		reader = csv.reader(open(inp,"r"))
		for row in reader:
			allGID.append(row)
	else: #input is provided as a list
		allGID = inp 

	#aids = GP.getAnnotID(allGID)
	# Extracts all the annotation ID's from IBEIS
	#GidAidMap = {allGID[i] : aids[i] for i in range(0,len(allGID))}
	gidInd = 0
	GidAidMap = {}
	for gid in allGID:
		aid = GP.getAnnotID(int(gid))
		GidAidMap[gid] = [aid]
		gidInd += 1
		percentComplete = gidInd * 100 / len(allGID)
		if math.floor(percentComplete) %5 == 0:
			printCompltnPercent(percentComplete)
	print()	
	print("Extracted all annotation ID's for selected images.")

	# filter out all the non-NONE annotation ids
	aidList = []
	for gid in GidAidMap.keys():
		for aid in filter(lambda x: x != None,GidAidMap[gid]):
			aidList = aidList + aid

	# Extracts all feature info based on annotation ID's from IBEIS
	features = {}
	print("Features to be extracted for %d annotation IDs" %len(aidList))
	nids = GP.getImageFeature(aidList,"name/rowid")
	names = GP.getImageFeature(aidList,"name/text")
	species_texts = GP.getImageFeature(aidList,"species/text")
	sex_texts = GP.getImageFeature(aidList,"sex/text")
	age_months = GP.getImageFeature(aidList,"age/months")
	exemplar_flags = GP.getImageFeature(aidList,"exemplar")
	quality_texts = GP.getImageFeature(aidList,"quality/text")
	yaw_texts = GP.getImageFeature(aidList,"yaw/text")
	image_contrib_tags = GP.getImageFeature(aidList,"image/contributor/tag")

	features = {aidList[i] : [nids[i],names[i],species_texts[i],sex_texts[i],
				GP.getAgeFeatureReadableFmt(age_months[i]),str(exemplar_flags[i]),
				quality_texts[i],yaw_texts[i],image_contrib_tags[i]] 
				for i in range(0,len(aidList))}
	print()
	print("All features extracted.")

	# Build the all combined file
	GidAidFeatures = {}
	for gid in GidAidMap.keys():
		if GidAidMap[gid][0] == None:
			GidAidFeatures[gid] = None
		else:
			GidAidFeatures[gid] = []
			for aid in GidAidMap.get(gid)[0]:
				newAidFeatures = {}
				newAidFeatures[aid] = features[aid]
				GidAidFeatures[gid].append(newAidFeatures)

	writeFLTitle,writeFLExt = outFL.split('.csv')
	writeFLExt = 'csv'
	writeFLGidAidFl = writeFLTitle + "_gid_aid_map." + writeFLExt
	writeFLAidFeatureFl = writeFLTitle + "_aid_features." + writeFLExt
	writeFLGidAidFeatureFl = writeFLTitle + "_gid_aid_features." + writeFLExt

	# Snippet for writing image GID - annotation ID map to a csv file
	head = ['GID','ANNOTATION_ID']
	writeCsvFromDict(head,GidAidMap,writeFLGidAidFl)

	head = ['ANNOTATION_ID','NID','NAME','SPECIES','SEX','AGE_MONTHS','EXEMPLAR_FLAG','IMAGE_QUALITY','IMAGE_YAW']
	writeCsvFromDict(head,features,writeFLAidFeatureFl)

	head = ['GID','ANNOTATION_ID','FEATURES']
	writeCsvFromDict(head,GidAidFeatures,writeFLGidAidFeatureFl) 

	outFL = open((writeFLTitle + "_gid_aid_map.json"),"w")
	json.dump(GidAidMap,outFL,indent=4)
	outFL.close()

	outFL = open((writeFLTitle + "_aid_features.json"),"w")
	json.dump(features,outFL,indent=4)
	outFL.close()

	outFL = open((writeFLTitle + "_gid_aid_features.json"),"w")
	json.dump(GidAidFeatures,outFL,indent=4)
	outFL.close()

	print("Script completed.")


def __main__():
	allGidPart1 = list(map(str,list(range(1,5000))))

	print("Starting feature extraction for GIDs . . .Part1")
	buildFeatureFl(allGidPart1,"../data/full1.csv",False)

	print("Completed feature extraction . . .Part1")	

	print("Starting EXIF feature extraction for GIDs . . .Part1")
	buildExifFeatureFl(allGidPart1,"../data/imgs_exif_data_full1.json",False)
	print("Completed EXIF feature extraction . . .Part1")

	allGidPart2 = list(map(str,list(range(5000,9407))))

	print("Starting feature extraction for GIDs . . .Part2")
	buildFeatureFl(allGidPart2,"../data/full2.csv",False)

	print("Completed feature extraction . . .Part2")	

	print("Starting EXIF feature extraction for GIDs . . .Part2")
	buildExifFeatureFl(allGidPart2,"../data/imgs_exif_data_full2.json",False)
	print("Completed EXIF feature extraction . . .Part2")

	print("Combining part files to full files")
	DS.combineJson("../data/full1_gid_aid_map.json","../data/full2_gid_aid_map.json","../data/full_gid_aid_map.json")
	DS.combineJson("../data/full1_gid_aid_features.json","../data/full2_gid_aid_features.json","../data/full_gid_aid_features.json")
	DS.combineJson("../data/full1_aid_features.json","../data/full2_aid_features.json","../data/full_aid_features.json")
	DS.combineJson("../data/imgs_exif_data_full1.json","../data/imgs_exif_data_full2.json","../data/imgs_exif_data_full.json")

if __name__ == "__main__":
	__main__()	
