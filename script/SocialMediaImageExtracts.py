# Script for running in parallel
# Author : Sreejith Menon
# Email : smenon8@uic.edu

import flickrapi as f
from urllib.request import urlretrieve
from functools import partial
from multiprocessing.pool import Pool
import os, re, pandas as pd, sys, json, time
import DataStructsHelperAPI as DS
import http.client, urllib.request, urllib.parse

# Ref: http://www.impulseadventure.com/photo/exif-orientation.html
def rotation_to_orientation(theta):
    if theta == 0:
        return 1
    elif theta == 90:
        return 8
    else:
        return 6

def download_link(directory, url, fl_nm=None):
	if fl_nm == None:
		fl_nm = str(directory + str(os.path.basename(url)))
	else:
		fl_nm = str(directory + fl_nm + '.jpeg')

	if not os.path.isfile(fl_nm):
		try:
			urlretrieve(url, fl_nm)
		except Exception as e:
			return 

def createFlickrObj(flickrKeyFl):
	# creating Flickr Object
	with open(flickrKeyFl,"r") as keyFl:
	    jsonObj = json.load(keyFl)

	flickrObj = f.FlickrAPI(jsonObj['flickr_key'], jsonObj['flickr_secret_key'],format='json')

	return flickrObj

def searchInFlickr(flickrObj, tags=[], text=None, page=1):
	print("Scraping from page %d" %page)
	photosJson = json.loads(flickrObj.photos.search(tags=tags, text=text, privacy_filter=1, page=page, per_page=500).decode(encoding='utf-8'))

	photos = photosJson['photos']['photo']
	urlList = []
	photoID = []
	for i in range(len(photos)):
	    dct = photos[i]
	    url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' %(str(dct['farm']),dct['server'],dct['id'],dct['secret'])
	    photoID.append(dct['id'])
	    urlList.append(url)

	return urlList, photoID

def multiProcMeth(methodName, arg, urlList, flNmList):
	start_time = time.time()

	download = partial(methodName, arg)
	with Pool(1) as p:
		p.starmap(download, zip(urlList, flNmList))

	print("Time elapsed: %f" %(time.time() - start_time))


def _getExif(flickrObj, photo_id):
	exifJson = json.loads(flickrObj.photos.getInfo(photo_id = photo_id).decode('utf-8'))
	
	lat = long = rotation = 0.0
	date = '1900-01-01 00:00:00'

	if exifJson['stat'] == 'ok':
		if 'location' in exifJson['photo'].keys():
			lat = exifJson['photo']['location']['latitude']
			long = exifJson['photo']['location']['longitude']
		if 'dates' in exifJson['photo']:
			date = exifJson['photo']['dates']['taken']
		if 'rotation' in exifJson['photo']:
			rotation = exifJson['photo']['rotation']

	sizeJson = json.loads(flickrObj.photos.getSizes(photo_id = photo_id).decode('utf-8'))

	width = height = 0

	if sizeJson['stat'] == 'ok':
		sizes = sizeJson['sizes']['size']
		for size in sizes:
			if size['label'] == 'Original':
				width = size['width']
				height = size['height']
				break
			if size['label'] == 'Large':
				width = size['width']
				height = size['height']
	
	return dict (lat =  float(lat), long = float(long), date = date, height = int(height), width = int(width), rotation = int(rotation))


def getExif(flickrObj, outFl, urlList=None, fileList=None):
	if urlList != None:
		photo_ids = [re.findall(r'.*/(.*)_.*_b.jpg', url)[0] for url in urlList]
	elif fileList != None:
		photo_ids = [re.findall(r'([0-9]*)_.*',fl)[0] for fl in fileList]

	fullExifData = {}
	for photo in photo_ids:
		print("Pull started for %s" %photo)
		fullExifData[photo] = _getExif(flickrObj, photo)
		time.sleep(1)
	with open(outFl,"w") as jsonFl:
		json.dump(fullExifData, jsonFl, indent = 4)

	return None

def scrape_flickr(to_page, out_fl_nm):
	urlListMaster = []
	for i in range(1,to_page):
		print("Scraping from page %d" %i)
		urlList,photoIDList = searchInFlickr(createFlickrObj("/Users/sreejithmenon/Google Drive/CodeBase/flickr_key.json"),["giraffe"],None,i)
		print(len(urlList))
		urlListMaster.extend(urlList)
	
	urlListMaster = list(set(urlListMaster))

	with open(out_fl_nm,"w") as urlListFl:
		for url in urlListMaster:
			urlListFl.write(url + "\n")

def download_imgs(urlFlList = "../data/fileURLS.dat"):
	with open(urlFlList,"r") as urlListFl:
		urlList = [url for url in urlListFl.read().split("\n")]

	download_dir = "/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/Flickr_Scrape_Giraffes/"

	idxs = [i for i in range(0,len(urlList),200)]

	for i in range(1,len(idxs)):
		print("Downloading from range %i to %i" %(idxs[i-1],idxs[i]-1))
		multiProcMeth(download_link, download_dir, urlList[idxs[i-1]:idxs[i]], [None]*200)

	print("Downloading last chunk")
	multiProcMeth(download_link, download_dir, urlList[4400:len(urlList)-1], [None]*19)

	return 

def download_imgs_bing(img_id_url_dict):
	download_dir = "/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/Bing_Scrape/"

	for key in img_id_url_dict.keys():
		download_link(download_dir, img_id_url_dict[key], key)

	return 

def get_exif_bing(search_result_value, out_fl_nm):
	img_exif = {}

	for result in search_result_value:
		img_exif[result['imageId']] = dict(width=result['width'], height=result['height'], date=result['datePublished'])

	with open(out_fl_nm, "w") as out_fl:
		json.dump(img_exif, out_fl, indent=4)

	return 

def get_search_results_bing(query, count=10, offset=0):
	with open("/Users/sreejithmenon/Google Drive/CodeBase/BingSearchAPI_key.dat", "r") as key_fl:
		key = key_fl.read()

	headers = {
    	'Ocp-Apim-Subscription-Key': key
	}
	params = urllib.parse.urlencode({
	    'q': query,
	    'count': count,
	    'offset': offset,
	    'mkt': 'en-us',
	    'safeSearch': 'Moderate'
	})

	try:
	    conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
	    conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
	    response = conn.getresponse()
	    data = response.read().decode('utf-8')
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return json.loads(data)

''' 
	Converting all that we have into a unified form
	The main identifier should be GID and not file name
	Below code will convert the EXIF file (and also beauty file) indexed by GID. 
'''
def convert_fl_gid_idx(inFl, outFl):
	with open("../data/flickr_imgs_gid_flnm_map.json", "r") as gid_fl_nm_map_fl:
		gid_flnm_map = json.load(gid_fl_nm_map_fl)

	flnm_gid_map = DS.flipKeyValue(gid_flnm_map)
	flnm_gid_map = {re.findall(r'([0-9]+)_.*', key)[0] : flnm_gid_map[key] for key in flnm_gid_map.keys()}

	with open(inFl, "r") as in_fl_obj:
		in_json_obj = json.load(in_fl_obj)

	out_json_obj = {}
	for key in in_json_obj.keys():
		out_json_obj[flnm_gid_map[key]] = in_json_obj[key]

	with open(outFl, "w") as out_fl_obj:
		json.dump(out_json_obj, out_fl_obj, indent=4)

	return 0


def bing_search_pipeline():
	next_offset = 0
	for i in range(50):
		search_results = get_search_results_bing("grevy's zebra", 150, 150*i + next_offset)
		print(len(search_results['value']))
		get_exif_bing(search_results['value'], "../data/bing_img_exif_%i.json" %i)
		next_offset = search_results['nextOffsetAddCount']

		img_id_url_dict = {result['imageId'] : result['contentUrl'] for result in search_results['value']}
		print("Download starting, Iteration %i..!" %(i+1))
		download_imgs_bing(img_id_url_dict)
		print()
		time.sleep(5)

	return 0

def __main__():
	# with open("../data/fileURLS.dat","r") as urlListFl:
	# 	urlList = [url for url in urlListFl.read().split("\n")]

	with open("../data/flickr_imgs_gid_flnm_map_new.json", "r") as flJson:
		flListJson = json.load(flJson)
	flList = list(flListJson.values())

	for i in range(0,len(flList),150):
		print("Extraction for %s to %s" %(i, min(i+150, len(flList))))
		getExif(createFlickrObj("/Users/sreejithmenon/Google Drive/CodeBase/flickr_key.json"), "../data/Flickr_EXIF_%s.json" %i , fileList = flList[i:min(i+150, len(flList))])
		time.sleep(5)

if __name__ == "__main__":
	# __main__()
	# scrape_flickr(51, "../data/file_urls_giraffes.dat")

	download_imgs("../data/file_urls_giraffes.dat")


	''' 
	Converting all that we have into a unified form
	The main identifier should be GID and not file name
	Below code will convert the EXIF file (and also beauty file) indexed by GID. 
	'''
	# convert_fl_gid_idx("../data/Flickr_EXIF_full.json", "../data/Flickr_EXIF_full.json")

	# bing_search_pipeline()