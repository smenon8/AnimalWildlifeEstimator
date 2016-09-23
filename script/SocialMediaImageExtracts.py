# Script for running in parallel
# Author : Sreejith Menon
# Email : smenon8@uic.edu

import json
import flickrapi as f

def createFlickrObj(flickrKeyFl):
	# creating Flickr Object
	with open(flickrKeyFl,"r") as keyFl:
	    jsonObj = json.load(keyFl)

	flickrObj = f.FlickrAPI(jsonObj['flickr_key'], jsonObj['flickr_secret_key'],format='json')

	return flickrObj

def searchInFlickr(flickrObj,tags=[],text=None):
	photosJson = json.loads(flickrObj.photos.search(tags=tags,text=text,privacy_filter=1).decode(encoding='utf-8'))

	photos = photosJson['photos']['photo']
	urlList = []
	for i in range(len(photos)):
	    dct = photos[i]
	    url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' %(str(dct['farm']),dct['server'],dct['id'],dct['secret'])
	    urlList.append(url)

	return urlList

def __main__():
	urlList = searchInFlickr(createFlickrObj("/Users/sreejithmenon/Google Drive/Project/flickr_key.json"),["giraffe","zebra"],"masai")
	print(urlList)

if __name__ == "__main__":
	__main__()