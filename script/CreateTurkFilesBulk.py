
# coding: utf-8

# ### Script for creating the m-turk files in bulk
# 
# There are 58 unique contributors and each contributor has a contiguous set of image contributions
# 
# Get contributed images per user:
# http://pachy.cs.uic.edu:5000/api/contributor/gids/?contrib_rowid_list=[1]
# 
# Get all contributor IDs
# http://pachy.cs.uic.edu:5000/api/contributor/valid_rowids/

import csv
import ComputeBiasStatsAPI as CB
import GenerateMTurkFileAPI as GM
import importlib
import random

# un-comment if there are any changes made to API
importlib.reload(CB) 
importlib.reload(GM) 


contributorImages = {}
for contributor in range(1,59):
     contributorImages[contributor] = CB.getContributorGID(contributor)

contributorImages.pop(52)
contributorImages.pop(57)
contributorImages.pop(8)
contributorImages.pop(11)
contributorImages.pop(17)
contributorImages.pop(32)
contributorImages.pop(34)
contributorImages.pop(41)

contributors = list(contributorImages.keys())

selectedImgContributors = []
for i in range(100):
    selectedImgContributors.append(contributors[random.randrange(0,50)])


argToAPI = []
for index in selectedImgContributors:
    imgList = contributorImages[index]
    minGID = min(imgList)
    maxGID = max(imgList)
    argToAPI.append([index,minGID,maxGID])

jobImageMap= {}

for i in range(0,100):
    flName = str("photo_album_%d" %(i+1))
    tup = argToAPI[i]
    slctdImgs = GM.generateMTurkFile(tup[1],tup[2],str("/tmp/files/" + flName),True)
    jobImageMap[flName] = slctdImgs
    i += 1
    
    inFL = open("files/sampleInput.txt","r")
    outFL = open(str("/tmp/files/" + flName+ ".input"),"w")
    for line in inFL:
            outFL.write(line)
    inFL.close()
    outFL.close()

    print("Successfully written : " + flName)

writeFL = open("/tmp/imageGID_job_map.csv","w")
writer = csv.writer(writeFL)
for key in jobImageMap:
    writer.writerow([key] + [jobImageMap[key]])

writeFL.close()