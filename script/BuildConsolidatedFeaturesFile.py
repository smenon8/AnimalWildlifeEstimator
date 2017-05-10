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

from __future__ import print_function
import GetPropertiesAPI as GP
import importlib, json, re, sys, csv, time
#importlib.reload(GP) # un-comment if there are any changes made to API
import pandas as pd
# import DataStructsHelperAPI as DS
from math import floor
# importlib.reload(GP)
from multiprocessing import Process
import DataStructsHelperAPI as DS
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
	width = GP.getExifData(gids,'width')
	height = GP.getExifData(gids,'height')
	orientation = GP.getExifData(gids,'orientation')
	size = GP.getExifData(gids,'size')


	imgProps = {gids[i] : {'datetime' : GP.getUnixTimeReadableFmt(datetimes[i]),
                      'lat' : lats[i],
                      'long' : longs[i],
                      'width' : width[i],
                      'height' : height[i],
                      'orientation' : orientation[i],
                      'size' : size[i]
                      } 
           for i in range(0,len(gids))}

	with open(outFL,"w") as outFl:
	    json.dump(imgProps,outFl,indent=4)

	return None

def buildBeautyFtrFl(inpFl, ftrs, outFlPrefix):
	df = pd.DataFrame.from_csv(inpFl).transpose().reset_index()
	df['index'] = df['index'].apply(lambda x : floor(float(x)))
	df.columns = ftrs
	df['GID'] = df['GID'].apply(lambda x : str(int(x)))
	df.to_csv(str(outFlPrefix + ".csv"),index=False)
	df.index=df['GID']
	df.drop(['GID'],1,inplace=True)

	dctObj = df.to_dict(orient='index')

	with open(str(outFlPrefix + ".json"),"w") as jsonObj:
	    json.dump(dctObj,jsonObj,indent=4)

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

def getAdditionalAnnotFeatures(gidAidMap, ftrName, outFlNm='/tmp/getAdditionalAnnotFeatures.dump.json'):
	with open(gidAidMap,"r") as gidAidMapFl:
		gidAidJson = json.load(gidAidMapFl)

	additionalFtrDct = {}
	gidInd = 0
	n = len(gidAidJson.keys())
	for gid in gidAidJson.keys():
		additionalFtrDct[gid] = additionalFtrDct.get(gid,[]) + [GP.getImageFeature(gidAidJson[gid][0],ftrName)][0]
		gidInd += 1
		percentComplete = gidInd * 100 / n
		if math.floor(percentComplete) %5 == 0:
			printCompltnPercent(percentComplete)

	with open(outFlNm,"w") as outFlObj:
		json.dump(additionalFtrDct, outFlObj, indent=4)

	return None
'''
Logic for reading data from the consolidatedHITResults file - changed
The input for the below method will be a csv file/list with all the image GID's for which the features have to be extracted.
'''
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

	features = {aidList[i] : {'nid' : nids[i],"name" : names[i],"species" : species_texts[i],"sex" : sex_texts[i],
				'age' : GP.getAgeFeatureReadableFmt(age_months[i]), 'exemplar': str(exemplar_flags[i]),
				'quality' : quality_texts[i],'yaw' : yaw_texts[i],'contributor' : image_contrib_tags[i]}
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

# these APIs require encoded annot_uuid_list
ggr_eco_ftr_api_map = {'age' : "/api/annot/age/months/json", 
					'sex': "/api/annot/sex/text/json",
					'bbox': "/api/annot/bbox/json", 
					'nid':  "/api/annot/name/rowid/json", 
					'exemplar': "/api/annot/exemplar/json",
					'species' : "/api/annot/species/json",
					'quality' : "/api/annot/quality/text/json",
					'view_point' : "/api/annot/yaw/text/json"
				}

# these APIs takes in an encoded gid list
ggr_otr_ftr_api_map = {'contributor' : "/api/image/note",
				'lat' : "/api/image/lat",
				'long' : "/api/image/lon",
				'datetime' : "/api/image/unixtime",
				'width' : "/api/image/width",
				'height' : "/api/image/height",
				'orientation' : "/api/image/orientation"
				}

def check_time_elapsed(start_time):
	if time.time() - start_time >= 1.0:
		return True
	else:
		return False

def build_feature_file_ggr(in_file, out_fl_head, start_count, end_count):
	with open(in_file, "r") as in_fl: 
		img_uuids = list(json.load(in_fl).keys())
	# img_uuids = [re.findall(r'(.*).jpg', uuid)[0] for uuid in img_uuids][start_count:end_count+1] # extract the filename without the extension
	img_uuids = [uuid for uuid in img_uuids][start_count:end_count+1] 

	print("Starting extract: %i to %i" %(start_count, end_count))
	start_time = time.time()
	uuid_annot_uuid_map = {}
	for img_uuid in img_uuids:
		uuid_dict = GP.ggr_get("/api/image/annot/uuid/json", GP.ggr_image_form_arg(img_uuid))
		if len(uuid_dict['results'][0]) == 0: # case 1: has no annotation
			uuid_annot_uuid_map[img_uuid] = [None]
		else: # case 2, has 1 or more annot
			for annot_dict in uuid_dict['results'][0]:
				uuid_annot_uuid_map[img_uuid] = uuid_annot_uuid_map.get(img_uuid, []) + [annot_dict["__UUID__"]]

		# elapsed time check
		if check_time_elapsed(start_time):
			start_time = time.time()
			print("100 seconds elapsed..!")
	
	print("Annotation UUIDs extracted")
	# logic to flatten out the list of lists
	aid_uuid_list = [item for sublist in list(uuid_annot_uuid_map.values()) for item in sublist if item]
	
	start_time = time.time()
	aid_uuid_feature_map = {}
	for aid in aid_uuid_list:
		species = GP.ggr_get(ggr_eco_ftr_api_map['species'], GP.ggr_annot_form_arg(aid))['results'][0] 
		sex = GP.ggr_get(ggr_eco_ftr_api_map['sex'], GP.ggr_annot_form_arg(aid))['results'][0]
		age = GP.getAgeFeatureReadableFmt(GP.ggr_get(ggr_eco_ftr_api_map['age'], GP.ggr_annot_form_arg(aid))['results'][0])
		bbox = GP.ggr_get(ggr_eco_ftr_api_map['bbox'], GP.ggr_annot_form_arg(aid))['results'][0]
		exemplar = GP.ggr_get(ggr_eco_ftr_api_map['exemplar'], GP.ggr_annot_form_arg(aid))['results'][0]
		nid = GP.ggr_get(ggr_eco_ftr_api_map['nid'], GP.ggr_annot_form_arg(aid))['results'][0]
		quality = GP.ggr_get(ggr_eco_ftr_api_map['quality'], GP.ggr_annot_form_arg(aid))['results'][0]
		view_point = GP.ggr_get(ggr_eco_ftr_api_map['view_point'], GP.ggr_annot_form_arg(aid))['results'][0]

		aid_uuid_feature_map[aid] = dict(sex=sex, age=age, bbox=bbox, exemplar=exemplar, nid=nid, species=species, view_point=view_point, quality=quality)	
		if check_time_elapsed(start_time):
			start_time = time.time()
			print("100 seconds elapsed..!")

	print("Feature extraction completed..!")

	uuid_annot_uuid_map_fl_nm = out_fl_head + "_uuid_annot_uuid_map.json"
	with open(uuid_annot_uuid_map_fl_nm, "w") as uuid_annot_uuid_map_fl:
		json.dump(uuid_annot_uuid_map, uuid_annot_uuid_map_fl, indent=4)

	annot_uuid_ftr_map_fl_nm = out_fl_head + "_annot_uuid_ftr_map.json"
	with open(annot_uuid_ftr_map_fl_nm, "w") as annot_uuid_ftr_map_fl:
		json.dump(aid_uuid_feature_map, annot_uuid_ftr_map_fl, indent=4)

	return 0

def build_exif_ftrs_fl_ggr(in_file_uuid_gid_map, in_file_uuid_list, out_fl, start, end):
	with open(in_file_uuid_gid_map, "r") as in_map_fl:
		uuid_gid_map = json.load(in_map_fl)

	with open(in_file_uuid_list, "r") as in_list_fl:
		uuid_list = in_list_fl.read().split("\n")[start:end+1]

	start_time = time.time()
	gid_uuid_exif_ftr_map = {}
	for uuid in uuid_list:
		gid = uuid_gid_map[uuid]
		lat = GP.ggr_get(ggr_otr_ftr_api_map['lat'], GP.ggr_gid_form_arg(gid))['results'][0]
		long = GP.ggr_get(ggr_otr_ftr_api_map['long'], GP.ggr_gid_form_arg(gid))['results'][0]
		datetime = GP.getUnixTimeReadableFmt(GP.ggr_get(ggr_otr_ftr_api_map['datetime'], GP.ggr_gid_form_arg(gid))['results'][0])
		contributor = GP.ggr_get(ggr_otr_ftr_api_map['contributor'], GP.ggr_gid_form_arg(gid))['results'][0]
		height = GP.ggr_get(ggr_otr_ftr_api_map['height'], GP.ggr_gid_form_arg(gid))['results'][0]
		width = GP.ggr_get(ggr_otr_ftr_api_map['width'], GP.ggr_gid_form_arg(gid))['results'][0]
		orientation = GP.ggr_get(ggr_otr_ftr_api_map['orientation'], GP.ggr_gid_form_arg(gid))['results'][0]

		gid_uuid_exif_ftr_map[uuid] = dict(lat=lat, long=long, datetime=datetime, contributor=contributor, height=height, width=width, orientation=orientation)
		if check_time_elapsed(start_time):
			start_time = time.time()
			print("100 seconds elapsed..!")

	with open(out_fl, "w") as uuid_exif_ftr_fl:
		json.dump(gid_uuid_exif_ftr_map, uuid_exif_ftr_fl, indent=4)

	return 0

def build_reqd_ftrs():


	return 0

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


def test(start, end, out):
	inExifFl,inGidAidMapFl,inAidFtrFl = "../data/ggr_gid_uuid_exif_ftr_map.json","../data/ggr_uuid_annot_uuid_map.json","../data/ggr_annot_uuid_ftr_map.json"
	with open(inGidAidMapFl, "r") as fl:
		obj = json.load(fl)


	with open(inAidFtrFl, "r") as fl:
	    obj2 = json.load(fl)

	no_ftr_annots = []

	for uuid in obj:
	    if obj[uuid][0] != None: #there is atleast one aid
	        for annot_id in obj[uuid]:
	            # check if annot_id in ftr file
	            if annot_id not in obj2.keys():
	                no_ftr_annots.append(annot_id)

	
	print(len(no_ftr_annots))         
	aid_uuid_feature_map = {}
	for aid in no_ftr_annots[start:end]:
		species = GP.ggr_get(ggr_eco_ftr_api_map['species'], GP.ggr_annot_form_arg(aid))['results'][0] 
		sex = GP.ggr_get(ggr_eco_ftr_api_map['sex'], GP.ggr_annot_form_arg(aid))['results'][0]
		age = GP.getAgeFeatureReadableFmt(GP.ggr_get(ggr_eco_ftr_api_map['age'], GP.ggr_annot_form_arg(aid))['results'][0])
		bbox = GP.ggr_get(ggr_eco_ftr_api_map['bbox'], GP.ggr_annot_form_arg(aid))['results'][0]
		exemplar = GP.ggr_get(ggr_eco_ftr_api_map['exemplar'], GP.ggr_annot_form_arg(aid))['results'][0]
		nid = GP.ggr_get(ggr_eco_ftr_api_map['nid'], GP.ggr_annot_form_arg(aid))['results'][0]
		quality = GP.ggr_get(ggr_eco_ftr_api_map['quality'], GP.ggr_annot_form_arg(aid))['results'][0]
		view_point = GP.ggr_get(ggr_eco_ftr_api_map['view_point'], GP.ggr_annot_form_arg(aid))['results'][0]

		aid_uuid_feature_map[aid] = dict(sex=sex, age=age, bbox=bbox, exemplar=exemplar, nid=nid, species=species, view_point=view_point, quality=quality)	

	with open(out, "w") as fl:
		json.dump(aid_uuid_feature_map, fl, indent=4)

if __name__ == "__main__":
	# gids = list(map(str, list(range(1,1702))))
	# buildFeatureFl(gids, "../data/Flickr_IBEIS_Ftrs.csv", False)
	# __main__()	
	# gidAidMapFl = "../data/full_gid_aid_map.json"
	# getAdditionalAnnotFeatures(gidAidMapFl,'bbox',"../data/gid_bbox.json")

	# buildBeautyFtrFl("../data/beautyFeatures_GZC_R.csv",['GID','pleasure','arousal','dominance','y'],"../data/beautyFeatures_GZC")

	# DS.combineJson("../data/beautyFeatures_GZC.json","../data/imgs_exif_data_full.json","../data/GZC_exifs_beauty_full.json")
	# p1 = Process(target=build_exif_ftrs_fl_ggr, args=("uuid_gid_map.json", "ggr_uuid_list.dat", "ggr_exif_extract_1.json",1,5000))
	# p2 = Process(target=build_exif_ftrs_fl_ggr, args=("uuid_gid_map.json", "ggr_uuid_list.dat", "ggr_exif_extract_2.json",5001,10000))
	# p3 = Process(target=build_exif_ftrs_fl_ggr, args=("uuid_gid_map.json", "ggr_uuid_list.dat", "ggr_exif_extract_3.json",10001,15000))
	# p4 = Process(target=build_exif_ftrs_fl_ggr, args=("uuid_gid_map.json", "ggr_uuid_list.dat", "ggr_exif_extract_4.json",15001,20000))
	# p5 = Process(target=build_exif_ftrs_fl_ggr, args=("uuid_gid_map.json", "ggr_uuid_list.dat", "ggr_exif_extract_5.json",20001,25000))
	# p6 = Process(target=build_exif_ftrs_fl_ggr, args=("uuid_gid_map.json", "ggr_uuid_list.dat", "ggr_exif_extract_6.json",25001,30000))
	# p7 = Process(target=build_exif_ftrs_fl_ggr, args=("uuid_gid_map.json", "ggr_uuid_list.dat", "ggr_exif_extract_7.json",30001,35000))
	# p8 = Process(target=build_exif_ftrs_fl_ggr, args=("uuid_gid_map.json", "ggr_uuid_list.dat", "ggr_exif_extract_8.json",35001,37433))

	# p9 = Process(target=build_feature_file_ggr, args=("uuid_gid_map.json", "ggr_ftr_extract_1",1,5000))
	# p10 = Process(target=build_feature_file_ggr, args=("uuid_gid_map.json", "ggr_ftr_extract_2",5001,10000))
	# p11 = Process(target=build_feature_file_ggr, args=("uuid_gid_map.json", "ggr_ftr_extract_3",10001,15000))
	# p12 = Process(target=build_feature_file_ggr, args=("uuid_gid_map.json", "ggr_ftr_extract_4",15001,20000))
	# p13 = Process(target=build_feature_file_ggr, args=("uuid_gid_map.json", "ggr_ftr_extract_5",20001,25000))
	# p14 = Process(target=build_feature_file_ggr, args=("uuid_gid_map.json", "ggr_ftr_extract_6",25001,30000))
	# p15 = Process(target=build_feature_file_ggr, args=("uuid_gid_map.json", "ggr_ftr_extract_7",30001,35000))
	# p16 = Process(target=build_feature_file_ggr, args=("uuid_gid_map.json", "ggr_ftr_extract_8",35001,37433))

	p1 = Process(target=test, args=(0, 400, "/tmp/test1.json"))
	p2 = Process(target=test, args=(400, 800, "/tmp/test2.json"))
	p3 = Process(target=test, args=(800, 1200, "/tmp/test3.json"))
	p4 = Process(target=test, args=(1200, 1600, "/tmp/test4.json"))
	p5 = Process(target=test, args=(1600, 2000, "/tmp/test5.json"))
	p6 = Process(target=test, args=(2000, 2400, "/tmp/test6.json"))
	p7 = Process(target=test, args=(2400, 2800, "/tmp/test7.json"))
	p8 = Process(target=test, args=(2800, 3200, "/tmp/test8.json"))
	p9 = Process(target=test, args=(3200, 3600, "/tmp/test9.json"))
	p10 = Process(target=test, args=(3600, 4033, "/tmp/test10.json"))

	p1.start()
	p2.start()
	p3.start()
	p4.start()
	p5.start()
	p6.start()
	p7.start()
	p8.start()
	p9.start()
	p10.start()
	# p11.start()
	# p12.start()
	# p13.start()
	# p14.start()
	# p15.start()
	# p16.start()
	