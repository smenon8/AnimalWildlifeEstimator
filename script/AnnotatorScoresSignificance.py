# python3

import JobsMapResultsFilesToContainerObjs as JRS
from nltk.metrics.agreement import AnnotationTask
from collections import OrderedDict
import re
import importlib
importlib.reload(JRS)
import pandas as pd
from math import ceil
import sys

## This function calculates the agreeability of share patterns across different albums
## i.e. to what degree do albums agree on the same images.
def getReliabilityMatImg(gidAlbumMapFl):
	results = JRS.createResultDict(1,100)
	imgAlbumDict = JRS.genImgAlbumDictFromMap(gidAlbumMapFl)
	
	imgShareCounts,_ = JRS.imgShareCountsPerAlbum(imgAlbumDict,results)

	imgShareCounts = list(filter(lambda row: row[4]>=80.0 or row[4] <= 20.0,imgShareCounts))
	reliability_matrix = [(row[0],row[1],1 if row[4]>=80 else 0) for row in imgShareCounts]

	return reliability_matrix


## This function returns reliability matrix for calculating if turkers agree on the way the same image is shared.
## i.e. to what degree do turkers agree on the same images
def getReliabilityMatTurker():
	print("Constructing reliability matrix")

	resultDict = JRS.createResultDict(1,100,workerData=True)

	reliabilityMatrx = []

	for album in resultDict.keys(): # loop 1
	    responses = resultDict[album]
	    workers = responses['workerid']
	    for response in responses.keys(): # loop 2
	        if 'Answer' in response and response.split(".")[1].isdigit():
	            shrNoShr = []
	            gid = response.split(".")[1]
	            for shrNShr in responses[response]: # loop 3.1
	                if len(shrNShr.split("|")) != 2: # no response captured
	                    shrNoShr.append("*")
	                elif shrNShr.split("|")[1] == 'share':
	                    shrNoShr.append(1)
	                else:
	                    shrNoShr.append(0)
	            
	            for i in range(len(workers)): # loop 3.2
	                reliabilityMatrx.append((workers[i],gid,shrNoShr[i]))	
	
	print("Constructing reliability matrix complete")
	
	return list(filter(lambda x : x[2] != '*',reliabilityMatrx))


def __main__(argv):
	if len(argv) != 2:
		print("Specify cmd arg")
		sys.exit(2)
	else:
		arg = argv[1]
		if arg == 'img':
			reliability_mat = getReliabilityMatImg("../data/imageGID_job_map_expt2_corrected.csv")
		else:
			reliability_mat = getReliabilityMatTurker()

		
		t = AnnotationTask(data=reliability_mat)

		print("Calculating the agreement scores")
		
		alpha = t.alpha()
		print("Alpha = %f" %alpha)
		
		s = t.S()
		print("S = %f" %s)

		pi = t.pi()
		print("Pi = %f" %pi)

		kappa = t.kappa()
		print("kappa = %f" %kappa)

if __name__ == "__main__":
	__main__(sys.argv)


