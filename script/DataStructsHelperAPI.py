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

	tot_keys = sum([len(list(flObj.keys())) for flObj in flObjs])

	for i in range(1,len(flObjs)):
		flObjs[0].update(flObjs[i])

	try:
		assert tot_keys == len(list(flObjs[0].keys()))
	except AssertionError:
		print("Length of input JSONs not equal to length of output Dict")

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
	d = appendJSON("../data/Flickr_Humpbacks_imgs_gid_flnm_map.json",
					"../data/Flickr_Humpbacks_imgs_gid_flnm_map_1.json")


	with open("../data/Flickr_Humpbacks_imgs_gid_flnm_map_comb.json", "w") as fl:
	    json.dump(d, fl, indent=4)

if __name__ == "__main__":
	__main__()
