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
	return datetime.strptime(dtStr,'%Y-%m-%d %H:%M:%S').date().strftime('%Y-%m-%d')

def combineJson(fl1,fl2,outFlNm):
	with open(fl1,"r") as f1, open(fl2,"r") as f2:
		jObj1 = json.load(f1)
		jObj2 = json.load(f2)

		for key in jObj1.keys():
			jObj1[key].update(jObj2[key])

		with open(outFlNm,"w") as out:
			json.dump(jObj1,out,indent=4)

	return None

def flipKeyValue(dct):
	outDct = {}

	for key in dct.keys():
		for val in dct[key]:
			outDct[val] = outDct.get(val,[]) + [key]

	return outDct
