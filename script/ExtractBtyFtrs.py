# python-3
# Author name: Sreejith Menon (smenon8@uic.edu)
# Creation date: December 01, 2016
# This script contains method to generate all beauty related features from images. 
# Very expensive when run serially.

from skimage import io, color, feature, transform
import numpy as np, pandas as pd
import time, json, argparse, math, os
from datetime import datetime
from sklearn.metrics.cluster import entropy

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

# logic to resize the image without affecting the aspect ratio
def resize_img(imgObj, base_width=600):
	if len(imgObj[0]) > 600:
		newHeight = int(len(imgObj) * base_width / len(imgObj[0]))
		return  transform.resize(imgObj, (newHeight,base_width))
	else: 
		return imgObj

def extr_beauty_ftrs(imgFlNm):
	# imgFlNm = "/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/All_Zebra_Count_Images/%s.jpeg" %gid
	img = os.path.basename(imgFlNm)
	
	try:
		rgbImg = resize_img(io.imread(imgFlNm))
	except Exception as e:
		print("Invalid image")
		return None
		
	if len(rgbImg.shape) != 3 or rgbImg.shape[2] !=3:
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
	ftrs['entropy'] = entropy(grayImg) # added to include entropy of the given image: more details: http://stackoverflow.com/a/42059758/5759063
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
	parser = argparse.ArgumentParser()
	parser.add_argument('-img_lst_fp', '--img_file_list_full_path', help='Full path to the image file list containing images list with full path', required=False)
	parser.add_argument('-path', '--img_file_folder_path', help='Path wehere all the image files are located', required=False)
	parser.add_argument('-img_lst', '--img_file_list', help='Full path to the image file list containing images list with only filenames', required=False)
	parser.add_argument('-out_fl', '--out_fl_nm', help='Full path to the output file', required=True)
	
	args = vars(parser.parse_args())

	out_fl = args["out_fl_nm"]

	if args["img_file_list_full_path"]:
		img_file_list = args["img_file_list_full_path"]
		with open(img_file_list, "r") as fl_list_fl:
			imgs = fl_list_fl.read().split("\n")
	elif args["img_file_folder_path"] and args["img_file_list"]:
		path = args["img_file_folder_path"]
		img_file_list = args["img_file_list"]
		with open(img_file_list, "r") as fl_list_fl:
			imgs = fl_list_fl.read().split("\n")
			imgs = [path + img for img in imgs]

	curr_start = start = time.time()
	for img in imgs:
		# print("Processing image : %s" %img)
		extr_beauty_ftrs(img)
		curr_time = time.time()
		if curr_time - curr_start > 100:
			curr_start = time.time()
			print("100 secs elapsed, processing %s" %img)

	with open(out_fl, "w") as outFl:
		json.dump(final_ftr_obj_global, outFl, indent = 4)

	end = time.time()

	print("Time elapsed: %f" %(end-start))

if __name__ == "__main__":
	__main__()
	#print(extr_beauty_ftrs("/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/All_Zebra_Count_Images/8598.jpeg"))