# coding: utf-8
# python-3

'''
Script for getting all images without duplicates from the csv file.
Author: Sreejith Menon
Date: May 23, 2016
'''

import csv
import BuildConsolidatedFeaturesFile as Features
import importlib
importlib.reload(Features)

def generateUniqueImageListFromMap(mapFlName):
	reader = csv.reader(open(mapFlName,"r"))
	head = reader.__next__()
	data = []
	for row in reader:
	    data.append(row)

	images = []
	for row in data:
		images += row[1:len(row)-1]

	uniqueImgs = list(set(images))

	return uniqueImgs




allUniqImgs = generateUniqueImageListFromMap("../data/imageGID_job_map_expt2_corrected.csv")
# outFL = "../data/all_imgs_expt2.csv"
# writeFL = open(outFL,"w")
# writer = csv.writer(writeFL)

# writer.writerow(allUniqImgs)

# writeFL.close()
Features.buildFeatureFl(allUniqImgs,"../data/experiment2.csv",False)
