# python-3
# Author name: Sreejith Menon (smenon8@uic.edu)
# Creation date: December 01, 2016
# This script contains method to generate all beauty related features from images. 
# Very expensive when run serially.

from skimage import io, color, feature, transform
import numpy as np
import time
import json
from BuildConsolidatedFeaturesFile import printCompltnPercent
import math
import pandas as pd
from datetime import datetime
import os

final_ftr_obj_global = {}
def calc_contrast(r, g, b):
	# y is the luminance
	y = 0.299 * r + 0.587 * g + 0.114 * b
	return (np.max(y) - np.min(y))/np.mean(y)

def get_spat_arrng_ftrs(gray_img):
	# resize img to 600 * 600
	resized_img = transform.resize(gray_img, (600,600))
	left = resized_img.transpose()[:300].transpose()
	right = resized_img.transpose()[300:].transpose()

	I_anti = np.identity(600)[::-1] # anti - diagonal identity matrix
	inner = feature.hog(left) - feature.hog(I_anti.dot(right))

	return dict(symmetry = np.linalg.norm(inner))

def calc_color_ftrs(h, s, v):
	v_mean = np.mean(v)
	s_mean = np.mean(s)

	# emotional features
	pleasure = 0.69 * v_mean + 0.22 * s_mean
	arousal =  -0.31 * v_mean + 0.60 * s_mean
	dominance = 0.76 * v_mean + 0.32 * s_mean

	# HSV-itten color histogram features
	counts_hue, _ = np.histogram(h, bins = 12) # 12 bins of hue
	counts_saturation, _ = np.histogram(s, bins = 5) # 5 bins of saturation
	counts_brightness, _ = np.histogram(v, bins = 3) # 3 bins of brightness (v)

	return dict(pleasure = pleasure, arousal = arousal, dominance = dominance, 
				hsv_itten_std_h = np.std(counts_hue), hsv_itten_std_s = np.std(counts_saturation), hsv_itten_std_v = np.std(counts_brightness))

def get_arr(imgObj):
	first = np.array([pix[0] for row in imgObj for pix in row])
	second = np.array([pix[1] for row in imgObj for pix in row])
	third = np.array([pix[2] for row in imgObj for pix in row])

	return (first, second, third)

def extr_beauty_ftrs(imgFlNm):
	# imgFlNm = "/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/All_Zebra_Count_Images/%s.jpeg" %gid
	img = os.path.basename(imgFlNm)
	
	rgbImg = io.imread(imgFlNm)
	if len(rgbImg.shape) != 3:
		print("Invalid image.. Continuing..")
		final_ftr_obj_global[img] = None
		return None

	hsvImg = color.rgb2hsv(rgbImg)
	grayImg = color.rgb2gray(rgbImg)

	red, green, blue = get_arr(rgbImg)
	hue, saturation, value = get_arr(hsvImg)

	contrast = calc_contrast(red, green, blue)
	ftrs = calc_color_ftrs(hue, saturation, value)
	ftrs['contrast'] = contrast
	ftrs.update(get_spat_arrng_ftrs(grayImg))
	
	final_ftr_obj_global[img] = ftrs
	
	return None

def createFtrFile(result_file, exif_file, out_fl):
	with open(exif_file,"r") as inpJsonFl:
		exifJsonObj = json.load(inpJsonFl)

	resultsDf = pd.DataFrame.from_csv(result_file)
	resultsDf = pd.DataFrame(resultsDf['Proportion']) 
	resultsDict = resultsDf.to_dict(orient="index")

	expt2Results = {}

	for gid in resultsDict:
	    expt2Results[str(gid)] = exifJsonObj[str(gid)]
	    expt2Results[str(gid)].update(resultsDict[gid])

	expt2ResultsDf = pd.DataFrame(expt2Results).transpose()

	expt2ResultsDf['datetime'] = expt2ResultsDf['datetime'].apply(lambda x : datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
	expt2ResultsDf['day'] = expt2ResultsDf.datetime.apply(lambda x : x.day)
	expt2ResultsDf['hour'] = expt2ResultsDf.datetime.apply(lambda x : x.hour)
	expt2ResultsDf.drop(['size','datetime'],1,inplace=True)
	
	expt2ResultsDf.to_csv(out_fl)

	return None

def __main__():
	path = "/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/Flickr_Scrape/"
	# with open("../data/fileURLS.dat","r") as urlListFl:
	# 	urlList = [url for url in urlListFl.read().split("\n")][1001:]

	# imgs = [path + os.path.basename(url) for url in urlList]
	with open("../data/new_flickr_extracts_fl_list.dat", "r") as fl_list_fl:
		imgs = fl_list_fl.read().split("\n")[2500:]

	imgs = [path + img for img in imgs]

	start = time.time()
	for img in imgs:
		print("Extraction started for %s" %img)
		extr_beauty_ftrs(img)
		

	with open("../data/beautyFeatures_FlickrExtracts_new_5.json", "w") as outFl:
		json.dump(final_ftr_obj_global, outFl, indent = 4)

	end = time.time()

	print("Time elapsed: %f" %(end-start))
	# ftr_extract = partial(extr_beauty_ftrs, final_ftr_obj)
	# with Pool(5) as p:
	# 	p.map(ftr_extract, gids)

	# print(final_ftr_obj)


if __name__ == "__main__":
	__main__()
	#print(extr_beauty_ftrs("/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/All_Zebra_Count_Images/8598.jpeg"))