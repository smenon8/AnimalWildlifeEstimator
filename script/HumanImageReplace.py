import csv
import GenerateMTurkFileAPI as GM
import webbrowser as W
import importlib
importlib.reload(GM) 

inFL = '../data/imageGID_job_map_expt2_mod.csv'
outFL = '../data/imageGID_job_map_expt2_corrected.csv'
excepFL = '../data/HumanImagesException.csv'

photoAlbumDict = {}
albumPhotoDict = {}

reader = csv.reader(open(inFL,"r"))
for row in reader:
    for i in range(1,len(row)):
        photoAlbumDict[row[i]] = photoAlbumDict.get(row[i],[]) + [row[0]]
        albumPhotoDict[row[0]] = albumPhotoDict.get(row[0],[]) + [row[i]]

humanImgJobMap = []

reader = csv.reader(open(excepFL,"r"))
for row in reader:
    humanImgJobMap.append((row[0],photoAlbumDict.get(str(row[0]),"Not found")))

humanImgJobMap = list(filter(lambda row: row[1] != "Not found",humanImgJobMap))


devFileReplace = open("sedCmdDev.sh","w")
prodFileReplace = open("sedCmdProd.sh","w")
oldNewImgMap = []

for row in humanImgJobMap:
	print("Finding replacement for image GID: %s" %row[0])
	for r in row[1]:
		print(r)
		imgList = albumPhotoDict[r]
		char = 'a'
		while char != 'q':
			start,end = int(min(imgList)),int(max(imgList))
			nextGID = GM.genRandomImg(start,end,imgList)
			
			url = "http://pachy.cs.uic.edu:5000/api/image/src/" + str(nextGID) + "/?resize_pix_w=300"
			W.open(url)
			
			char = input("Enter q to quit : ")
			
			# if q is entered, that means the image is approved
			if char == 'q':
				oldNewImgMap.append(row[0],)
				fileArg = r + "_prod.question"
				fileArgDev = r + ".question"
				
				oldImg = row[0]
				newImg = nextGID
		
				imgList.remove(str(oldImg))
				imgList.append(str(newImg))
				imgList = set(imgList)

				cmd = 'sed -i.bak "s/%s/%s/g" %s\n' %(oldImg,newImg,fileArg)
				cmdDev = 'sed -i.bak "s/%s/%s/g" %s \n' %(oldImg,newImg,fileArgDev)

				devFileReplace.write(cmdDev)
				prodFileReplace.write(cmd)

# Snippet for writing the corrected image list to a new file
writeFL = open(outFL,"w")
writer = csv.writer(writeFL)

for key in albumPhotoDict.keys():
    writer.writerow([key,albumPhotoDict[key]])

writeFL.close()

devFileReplace.close()
prodFileReplace.close()
