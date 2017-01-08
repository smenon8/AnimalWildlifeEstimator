# coding: utf-8
# python-3
# Author: Sreejith Menon (smenon8@uic.edu)


# Description: Contains a single method that generates mechanical turk jobs for generating photo-albums in bulk. 
# This script contains a __main__() method that accepts command line arguments and can be directly executed through terminal.
# To run the script provide 4 parameters in the order fileName, jobMapName, numberOfFiles, numberOfImgs.
# python CreateTurkFilesBulk.py /tmp/sample /tmp/sample.csv 2 10
# Successfully written : /tmp/sample1
# Successfully written : /tmp/sample2

import csv
import GetPropertiesAPI as GP
import GenerateMTurkFileAPI as GM
import importlib
import random
import sys

# un-comment if there are any changes made to API
importlib.reload(GP) 
importlib.reload(GM) 

# Selects noOfJobs number of random contributors (there might be duplicates in the selected contributor list). 
# There is hard-coded code for removing contributors who did not click any picture.
# For each job, noOfImgsPerJob number of images are selected from the range of images a particular contributor has clicked. 
# This is done to ensure that given a particular album, all the images are clicked by the same contributor. 
# The script assumes the value of prodFileWrite in line 63 as True. 
# It generates 1 input, 1 question file per noOfJobs and 1 map file that contains a map between albums and the images in them.
def createTurkFilesBulk(flNm,jobMapName,noOfJobs,noOfImgsPerJob = 20):
    contributorImages = {}
    for contributor in range(1,59):
        contributorImages[contributor] = GP.getContributorGID(contributor)

    contributorImages.pop(52)
    contributorImages.pop(57)
    contributorImages.pop(8)
    contributorImages.pop(11)
    contributorImages.pop(17)
    contributorImages.pop(32)
    contributorImages.pop(34)
    contributorImages.pop(41)
    print(len(contributorImages.keys()))
    contributors = list(filter(lambda x: len(contributorImages[x]) > 8, contributorImages.keys()))
    print(len(contributors))
    selectedImgContributors = []
    for i in range(0,noOfJobs):
        selectedImgContributors.append(contributors[random.randrange(0,len(contributors))])

    argToAPI = []
    for index in selectedImgContributors:
        imgList = contributorImages[index]
        minGID = min(imgList)
        maxGID = max(imgList)
        argToAPI.append([index,minGID,maxGID])


    jobImageMap= {}

    for i in range(0,noOfJobs):
        flName = str(flNm + str(i+1))
        tup = argToAPI[i]
        slctdImgs = GM.generateMTurkFile(tup[1],tup[2],str(flName),noOfImgsPerJob,True)
        jobImageMap[flName] = slctdImgs
        i += 1
        
        inFL = open("files/sampleInput.txt","r")
        outFL = open(str(flName+ ".input"),"w")
        for line in inFL:
                outFL.write(line)
        inFL.close()
        outFL.close()

        print("Successfully written : " + flName)

    writeFL = open(jobMapName,"w")
    writer = csv.writer(writeFL)
    for key in jobImageMap:
        writer.writerow([key] + [jobImageMap[key]])

    writeFL.close()

def __main__(args):
    if len(args) == 5:
        flName = args[1]
        jobMapName = args[2]
        numberOfFiles = int(args[3])
        numberOfImgs = int(args[4])
        createTurkFilesBulk(flName,jobMapName,numberOfFiles,numberOfImgs)
    else:
        print("Error: Provide 4 parameters in the order fileName, jobMapName, numberOfFiles, numberOfImgs")

if __name__ == "__main__":
    __main__(sys.argv)
    # createTurkFilesBulk("/tmp/test", "/tmp/map_test.csv", 5, 100)