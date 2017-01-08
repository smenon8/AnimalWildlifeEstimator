# Get results from mechanical turk
for i in range(1,101):
	inputFL = "photo_album_" + str(i) + ".input.success"
	outFL = "photo_album_" + str(i) + ".results"
	cmd = "call ​getResults -successfile %jobPath%\\" + inputFL + " -outputfile  %jobPath%\\" + outFL
	print(cmd)


# Approve all work
for i in range(1,101):
	inputFL = "photo_album_" + str(i) + ".input.success"
	cmd = "call approveWork -successfile %jobPath%\\" + inputFL
	print(cmd)
	
# ​getResults -successfile C:\Users\Sreejith\Downloads\Archive\photo_album_1.input.success -outputfile C:\Users\Sreejith\Downloads\mturk\photo_album_1.results

# approveWork -successfile C:\Users\Sreejith\Downloads\Archive\photo_album_1.input.success​

#Python script for create hit command
for i in range(1,101):
	inputFL = "Expt3_" + str(i) + ".input"
	questionFL ="Expt3_" + str(i) + ".question"
	cmd = "call loadHITs -input %jobPath%\\" + inputFL + " -question  %jobPath%\\" + questionFL + " -properties %jobPath%\photo_album.properties -sandbox"
	print(cmd)


for i in range(1,101):
	print("deleteHITs -successfile Exp3_%s.input.success -approve -expire -force" %i)