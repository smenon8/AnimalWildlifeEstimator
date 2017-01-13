# python-3
'''
Created on Tue May 24 16:04:40 2016

Author: Sreejith Menon (smenon8@uic.edu)

Description: Contains methods to generate a single mechanical turk photo album. 
There are multiple methods in the API but the method generateMTurkFile() needs to be called to generate one image album job file.
 
Hardcoded parameter: 
excepFL – points to the csv file which is a enumeration of all identified human images. 
This is provided to avoid occurrences of human images in the mechanical turk photo album jobs.
'''
import htmltag as HT
import random
from htmltag import table, td, tr
import sys
import csv

excepFL = '../data/HumanImagesException.csv'

# Arguments: Start range, End Range and list in the same range
# Returns: A randomly selected image GID in the range [begin, end] and not in oldList.
# This method is used when there arises a case when a particular image in the image album have to be replaced with another randomly selected image. 
def genRandomImg(begin,end,oldList):
    found = False
    
    # Human Image selection exception
    reader = csv.reader(open(excepFL,"r"))
    humanImgs = []
    for row in reader:
        humanImgs.append(int(row[0]))
    
    while not found:
        num = random.randrange(begin,end)
        if num in oldList or num in humanImgs: continue

        found = True

    return num

# Arguments: Start range, end range and number of images in photo album
# Returns: A python list with randomly selected image GID’s that are in the range [begin, stop] and len(list) = maxImgs
# This method is used to generate a list of random images that will be further used as an input to the method that generates the photo album mechanical turk job. 
# The list has no duplicates and has exactly maxImgs number of images.
def genImageList(begin,stop,maxImgs=20):
    count = 0
    listNum = []
    start= begin
    end = stop

    with open(excepFL,"r") as excpFl:
        reader = csv.reader(excpFl)
        humanImgs = []
        for row in reader:
            humanImgs.append(int(row[0]))

    listNum = list(range(begin, stop+1))

    finalGidList = [gid for gid in listNum if gid not in humanImgs] # remove all human images

    # if len(finalGidList) > maxImgs: # if there are more than 100 (maxImgs) images, then shuffle and select the first 100 (maxImgs) images
    #     random.shuffle(finalGidList)
    #     finalGidList = finalGidList[:maxImgs]
    # else: # otherwise select all images
    #     random.shuffle(finalGidList)
    random.shuffle(finalGidList)
    return finalGidList

# Arguments: Start GID, end GID, name of output file, number of images in photo album, a boolean to generate a m-turk job for production environment
# Returns: A python list with randomly selected image GID’s that are in the photo album. 
# The GID’s are in the range [startGID, endGID] and len(list) = maxImgs
# Most important method of this script. This generates a .question file that is fed to createHIT command. 
# If prodFileWrite parameter is set to True, then a job with the same image GID’s is generated with the word ‘prod’ appended to the outFile name. 
# prodFileWrite is defaulted to False, so it will only generate a file for mechanical turk sandbox if this parameter is unspecified.
def generateMTurkFile(startGID,endGID,outFile,maxImgs=20,prodFileWrite = False):
    imageIDList = genImageList(startGID,endGID,maxImgs)

    links = ["https://socialmediabias.blob.core.windows.net/wildlifephotos/All_Zebra_Count_Images/"+str(i)+".jpeg" for i in imageIDList]
    imgTags = []
    radioShare = HT.input
    for url in links:
        imgTags.append(HT.img(src = url,alt = "Unavailable"))

    # logic to create the radio buttons and the hidden form fields
    shareRadio = []
    notShareRadio = []
    hiddenField = []
    for i in range(len(imageIDList)):
        hiddenField.append(HT.input(type='hidden',name=imageIDList[i],value=imageIDList[i]))
        shareRadio.append(HT.input(type='radio',value='share',required=True,name=imageIDList[i]) + "Share")
        notShareRadio.append(HT.input(type='radio',value='noShare',required=True,name=imageIDList[i]) + "Do Not Share")

    tdTags = []
    for i in range(len(imageIDList)):
        tdTags.append(HT.td(HT.center(HT.HTML(hiddenField[i]),HT.HTML(shareRadio[i]),HT.HTML(notShareRadio[i])),HT.HTML(imgTags[i])))

    trTags = []
    for i in range(1,len(imageIDList),2):
        trTags.append(HT.tr(HT.HTML(tdTags[i-1]),HT.HTML(tdTags[i])))

    bodyTxt = HT.table(HT.HTML('\n'.join(trTags)),border="1")

    headFile = open("files/header.txt","r")
    tailFile = open("files/tail.txt","r")
    outFileDev = outFile + ".question"
    outputFile = open(outFileDev,"w")

    for line in headFile:
        outputFile.write(line)
        
    outputFile.write(bodyTxt)

    for line in tailFile:
        outputFile.write(line)

    headFile.close()
    tailFile.close()
    outputFile.close()

    if prodFileWrite:
        headFile = open("files/header_prod.txt","r")
        tailFile = open("files/tail_prod.txt","r")
        outFileProd = outFile + "_prod.question"
        outputFile = open(outFileProd,"w")
        for line in headFile:
            outputFile.write(line)
        
        outputFile.write(bodyTxt)

        for line in tailFile:   
            outputFile.write(line)

        headFile.close()
        tailFile.close()
        outputFile.close()
    print("job generation complete!")
    return imageIDList

def __main__():
    generateMTurkFile(4856,5000,"files/sample",100)

if __name__ == "__main__":
    __main__()
