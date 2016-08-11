'''
Script Name: DataStructsHelperAPI.py

Created date : Sunday, 11th August 2016
Author : Sreejith Menon (smenon8@uic.edu)
'''

import csv

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

# Generate dictionary with row[0] as key and row[1:] as value
# Generate dictionary object from JSON.