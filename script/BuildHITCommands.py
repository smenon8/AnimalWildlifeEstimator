# Get results from mechanical turk
for i in range(1,101):
	inputFL = "Expt3_photo_album_" + str(i) + ".input.success"
	outFL = "Expt3_photo_album_" + str(i) + ".results"
	cmd = "call ​getResults -successfile %jobPath%\\" + inputFL + " -outputfile  %jobPath%\\" + outFL
	print(cmd)


# Approve all work
for i in range(1,101):
	inputFL = "Expt3_photo_album_" + str(i) + ".input.success"
	cmd = "call approveWork -successfile %jobPath%\\" + inputFL
	print(cmd)
	
# ​getResults -successfile C:\Users\Sreejith\Downloads\Archive\photo_album_1.input.success -outputfile C:\Users\Sreejith\Downloads\mturk\photo_album_1.results

# approveWork -successfile C:\Users\Sreejith\Downloads\Archive\photo_album_1.input.success​

#Python script for create hit command
for i in range(1,101):
	inputFL = "Expt3_photo_album_" + str(i) + ".input"
	questionFL ="Expt3_photo_album_" + str(i) + "_prod.question"
	cmd = "call loadHITs -input %jobPath%\\" + inputFL + " -question %jobPath%\\" + questionFL + " -properties %jobPath%\photo_album.properties"
	print(cmd)


for i in range(1,101):
	print("deleteHITs -successfile Exp3_%s.input.success -approve -expire -force" %i)


#Python script for create hit command for *NIX platforms
for i in range(1,11):
	inputFL = "Expt3_photo_album_" + str(i) + ".input"
	questionFL ="Expt3_photo_album_" + str(i) + "_prod.question"
	cmd = "loadHITs.sh -input $jobPath/" + inputFL + " -question $jobPath/" + questionFL + " -properties $jobPath/photo_album.properties"
	print(cmd)
	print()


'''
export jobPath="/tmp"

bash loadHITs.sh -input $jobPath/Expt3_photo_album_1.input -question $jobPath/Expt3_photo_album_1_prod.question -properties $jobPath/photo_album.properties

bash loadHITs.sh -input $jobPath/Expt3_photo_album_2.input -question $jobPath/Expt3_photo_album_2_prod.question -properties $jobPath/photo_album.properties

bash loadHITs.sh -input $jobPath/Expt3_photo_album_3.input -question $jobPath/Expt3_photo_album_3_prod.question -properties $jobPath/photo_album.properties

bash loadHITs.sh -input $jobPath/Expt3_photo_album_4.input -question $jobPath/Expt3_photo_album_4_prod.question -properties $jobPath/photo_album.properties
bash 
bash loadHITs.sh -input $jobPath/Expt3_photo_album_5.input -question $jobPath/Expt3_photo_album_5_prod.question -properties $jobPath/photo_album.properties
bash 
bash loadHITs.sh -input $jobPath/Expt3_photo_album_6.input -question $jobPath/Expt3_photo_album_6_prod.question -properties $jobPath/photo_album.properties
bash 
bash loadHITs.sh -input $jobPath/Expt3_photo_album_7.input -question $jobPath/Expt3_photo_album_7_prod.question -properties $jobPath/photo_album.properties
bash 
bash loadHITs.sh -input $jobPath/Expt3_photo_album_8.input -question $jobPath/Expt3_photo_album_8_prod.question -properties $jobPath/photo_album.properties
bash 
bash loadHITs.sh -input $jobPath/Expt3_photo_album_9.input -question $jobPath/Expt3_photo_album_9_prod.question -properties $jobPath/photo_album.properties
bash 
bash loadHITs.sh -input $jobPath/Expt3_photo_album_10.input -question $jobPath/Expt3_photo_album_10_prod.question -properties $jobPath/photo_album.properties

'''