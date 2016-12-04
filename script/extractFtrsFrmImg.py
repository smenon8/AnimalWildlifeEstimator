from skimage import io, color, feature, transform
import numpy as np
import time
import json
from BuildConsolidatedFeaturesFile import printCompltnPercent
import math

final_ftr_obj = {}
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

def extr_beauty_ftrs(gid):
	imgFlNm = "/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/All_Zebra_Count_Images/%s.jpeg" %gid
	rgbImg = io.imread(imgFlNm)
	hsvImg = color.rgb2hsv(rgbImg)
	grayImg = color.rgb2gray(rgbImg)

	red, green, blue = get_arr(rgbImg)
	hue, saturation, value = get_arr(hsvImg)

	contrast = calc_contrast(red, green, blue)
	ftrs = calc_color_ftrs(hue, saturation, value)

	ftrs.update(get_spat_arrng_ftrs(grayImg))
	final_ftr_obj[gid] = ftrs
	
	return None

def __main__():
	gids = [i for i in range(1,9407)]

	start = time.time()
	for gid in gids:
		extr_beauty_ftrs(gid)
		percentComplete = gid * 100 / len(gids)
		if math.floor(percentComplete) % 2 == 0:
			printCompltnPercent(percentComplete)

	with open("../data/beautyFeatures_FlickrImgs.json", "w") as outFl:
		json.dump(final_ftr_obj, outFl, indent = 4)

	end = time.time()

	print("Time elapsed: %f" %(end-start))
	# ftr_extract = partial(extr_beauty_ftrs, final_ftr_obj)
	# with Pool(5) as p:
	# 	p.map(ftr_extract, gids)

	# print(final_ftr_obj)


if __name__ == "__main__":
	__main__()
	#print(extr_beauty_ftrs("/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/All_Zebra_Count_Images/8598.jpeg"))