import htmltag as HT
import random
from htmltag import table, td, tr
import sys

maxImgs = 20


def genImageID(begin,stop):
    count = 0
    listNum = []
    start= begin
    end = stop
    while count < maxImgs:
        num = random.randrange(start,end)
        if num in listNum: continue
        listNum.append(num)
        count += 1
    
    return listNum

def generateMTurkFile(startGID,endGID,outFile,prodFileWrite = False):
    imageID = genImageID(startGID,endGID)
    links = ["http://pachy.cs.uic.edu:5000/api/image/src/"+str(i)+"/?resize_pix_w=500" for i in imageID[0:maxImgs]]
    imgTags = []
    radioShare = HT.input
    for url in links:
        imgTags.append(HT.img(src = url,alt = "Unavailable"))

    # logic to create the radio buttons and the hidden form fields
    shareRadio = []
    notShareRadio = []
    hiddenField = []
    for i in range(maxImgs):
        hiddenField.append(HT.input(type='hidden',name=imageID[i],value=imageID[i]))
        shareRadio.append(HT.input(type='radio',value='share',name=imageID[i]) + "Share")
        notShareRadio.append(HT.input(type='radio',value='noShare',name=imageID[i]) + "Do Not Share")

    tdTags = []
    for i in range(maxImgs):
        tdTags.append(HT.td(HT.center(HT.HTML(hiddenField[i]),HT.HTML(shareRadio[i]),HT.HTML(notShareRadio[i])),HT.HTML(imgTags[i])))

    trTags = []
    for i in range(0,maxImgs,2):
        trTags.append(HT.tr(HT.HTML(tdTags[i]),HT.HTML(tdTags[i+1])))

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

    return imageID

def __main__(argv):
    generateMTurkFile(4856,4867,"files/sample.question")

if __name__ == "__main__":
    __main__(sys.argv)
