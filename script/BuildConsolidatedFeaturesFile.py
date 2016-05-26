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

	# Extracts all the annotation ID's from IBEIS
	GidAidMap = {}
	for gid in allGID:
		aid = GP.getAnnotID(int(gid))
		GidAidMap[gid] = [aid]

	print("Extracted all annotation ID's for selected images.")

	# filter out all the non-NONE annotation ids
	aidList = []
	for gid in GidAidMap.keys():
		for aid in filter(lambda x: x != None,GidAidMap[gid]):
			aidList = aidList + aid

	# Extracts all feature info based on annotation ID's from IBEIS
	features = {}
	for aid in aidList:
		nid = GP.getImageFeature(aid,"nids")
		features[aid] = [nid]
		names = GP.getImageFeature(aid,"names")
		features[aid].append(names)
		spec_text = GP.getImageFeature(aid,"species_texts")
		features[aid].append(spec_text)
		sex_text = GP.getImageFeature(aid,"sex_texts")
		features[aid].append(sex_text)
		est_age = GP.getImageFeature(aid,"age_months_est")
		features[aid].append(est_age)
		exemplar = GP.getImageFeature(aid,"exemplar_flags")
		features[aid].append(exemplar)
		qual_text = GP.getImageFeature(aid,"quality_texts")
		features[aid].append(qual_text)
		yaw_text = GP.getImageFeature(aid,"yaw_texts")
		features[aid].append(yaw_text)

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


	outFL = open("../data/gid_aid_features.json","w")
	json.dump(GidAidFeatures,outFL,indent=4)
	outFL.close()

	print("Script completed.")