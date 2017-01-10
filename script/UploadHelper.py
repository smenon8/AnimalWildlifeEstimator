import sys
import UploadAndDetectIBEIS as UD
import GetPropertiesAPI as GP
import json

def __main__(sys.argv):
	flListFl = sys.argv[1]
	with open(flListFl, "r") as flListFlObj:
		flList = flListFlObj.read().split("\n")

	print("Start upload..!")
	flGidMap = {UD.upload(fl) : fl for fl in flList} 
	# you will have a map/dictionary between all the gids and the file names that you have

	print("Finish upload..!")

	mapFlName = 'specify the file name'
	with open(mapFlName, "w") as mapFlObj:
		json.dump(flGidMap, mapFlObj, indent=4)

if __name__ == '__main__':
	__main__(sys.argv)

