# Script for running in parallel
# Author : Sreejith Menon
# Email : smenon8@uic.edu

import sys
import json
import flickrapi as f
from urllib.request import urlretrieve
from functools import partial
from multiprocessing.pool import Pool
import time
import os
from threading import Thread

def download_link(directory, url):
    flName = str(directory + str(os.path.basename(url)))
    if not os.path.isfile(flName):
    	urlretrieve(url, flName)

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

def multiProcMeth(methodName, arg, urlList):
	start_time = time.time()

	download = partial(methodName, arg)
	with Pool(5) as p:
		p.map(download, urlList)

	print("Time elapsed: %f" %(time.time() - start_time))

def __main__(argv):
	if len(argv) != 2:
		page = 1
	else:
		page = int(argv[1])

	urlListMaster = []
	for i in range(1,page):
		print("Scraping from page %d" %i)
		urlList,photoIDList = searchInFlickr(createFlickrObj("/Users/sreejithmenon/Google Drive/CodeBase/flickr_key.json"),["grevy's zebra"],None,i)
		print(len(urlList))
		urlListMaster.extend(urlList)
	
	print(len(urlListMaster))
	urlListMaster = list(set(urlListMaster))
	print(len(urlListMaster))
	with open("../data/fileURLS.dat","w") as urlListFl:
		for url in urlListMaster:
			urlListFl.write(url + "\n")


if __name__ == "__main__":
	# __main__(sys.argv)

	with open("../data/fileURLS.dat","r") as urlListFl:
		urlList = [url for url in urlListFl.read().split("\n")]

	download_dir = "/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/Flickr_Scrape/"

	idxs = [i for i in range(1400,len(urlList),200)]

	for i in range(1,len(idxs)):
		print("Downloading from range %i to %i" %(idxs[i-1],idxs[i]-1))
		multiProcDownload(download_link, download_dir, urlList[idxs[i-1]:idxs[i]])

	print("Downloading last chunk")
	print(urlList[1800:])
	multiProcDownload(download_link, download_dir, urlList[1800:len(urlList)-1])




