'''
Script Name: DataStructsHelperAPI.py

Created date : Sunday, 11th August 2016
Author : Sreejith Menon (smenon8@uic.edu)
'''

import csv
from datetime import datetime
import json

# Generate list of tuples from csv
def genlstTupFrmCsv(flNm,headerExists=True):
	with open(flNm,'r') as inFl:
		csvFl = csv.reader(inFl)
		if headerExists:
			header = csvFl.__next__()
		else:
			header = None
		return header,[tuple(row) for row in csvFl]

def cnvrtDictToLstTup(dct):
	return [(key,dct[key]) for key in dct.keys()]


# Generate Date(String) in outFmt from TimeStamp(String) in inpFmt
def getDateFromStr(dtStr,inpFmt,outFmt):
	return datetime.strptime(dtStr,inpFmt).date().strftime(outFmt)

def combineJSON(fl1,fl2,outFlNm):
	with open(fl1,"r") as f1, open(fl2,"r") as f2:
		jObj1 = json.load(f1)
		jObj2 = json.load(f2)

		for key in jObj1.keys():
			jObj1[key].update(jObj2[key])

		with open(outFlNm,"w") as out:
			json.dump(jObj1,out,indent=4)

	return None

def appendJSON(*inpFl):
	flObjs = []
	for fl in inpFl:
		with open(fl, "r") as jFl:
			flObjs.append(json.load(jFl))

	for i in range(1,len(flObjs)):
		flObjs[0].update(flObjs[i])

	return flObjs[0]


def flipKeyValue(dct):
	outDct = {}

	for key in dct.keys():
		if type(dct[key]) in [list, tuple]:
			for val in dct[key]:
				outDct[val] = outDct.get(val,[]) + [key]
		else:
			outDct[dct[key]] = key

	return outDct


def __main__():
	d = appendJSON("../data/Flickr_EXIF_0.json",
				"../data/Flickr_EXIF_150.json",
				"../data/Flickr_EXIF_300.json",
				"../data/Flickr_EXIF_450.json",
				"../data/Flickr_EXIF_600.json",
				"../data/Flickr_EXIF_750.json",
				"../data/Flickr_EXIF_900.json",
				"../data/Flickr_EXIF_1050.json",
				"../data/Flickr_EXIF_1200.json",
				"../data/Flickr_EXIF_1350.json",
				"../data/Flickr_EXIF_1500.json",
				"../data/Flickr_EXIF_1650.json",
				"../data/Flickr_EXIF_1800.json",
				"../data/Flickr_EXIF_1950.json",
				"../data/Flickr_EXIF_2100.json",
				"../data/Flickr_EXIF_2250.json",
				"../data/Flickr_EXIF_2400.json",
				"../data/Flickr_EXIF_2550.json",
				"../data/Flickr_EXIF_2700.json",
				"../data/Flickr_EXIF_2850.json",
				"../data/Flickr_EXIF_3000.json",
				"../data/Flickr_EXIF_3150.json",
				"../data/Flickr_EXIF_3300.json",
				"../data/Flickr_EXIF_3450.json",
				"../data/Flickr_EXIF_3600.json")


	with open("../data/Flickr_EXIF_Full_new.json", "w") as fl:
	    json.dump(d, fl, indent=4)

if __name__ == "__main__":
	__main__()
