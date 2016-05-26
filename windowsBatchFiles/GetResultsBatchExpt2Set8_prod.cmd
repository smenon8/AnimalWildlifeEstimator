@echo off
REM Windows batch file to get results on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call getResults -successfile %jobPath%\photo_album_71.input.success -outputfile  %jobPath%\photo_album_71.results
call getResults -successfile %jobPath%\photo_album_72.input.success -outputfile  %jobPath%\photo_album_72.results
call getResults -successfile %jobPath%\photo_album_73.input.success -outputfile  %jobPath%\photo_album_73.results
call getResults -successfile %jobPath%\photo_album_74.input.success -outputfile  %jobPath%\photo_album_74.results
call getResults -successfile %jobPath%\photo_album_75.input.success -outputfile  %jobPath%\photo_album_75.results
call getResults -successfile %jobPath%\photo_album_76.input.success -outputfile  %jobPath%\photo_album_76.results
call getResults -successfile %jobPath%\photo_album_77.input.success -outputfile  %jobPath%\photo_album_77.results
call getResults -successfile %jobPath%\photo_album_78.input.success -outputfile  %jobPath%\photo_album_78.results
call getResults -successfile %jobPath%\photo_album_79.input.success -outputfile  %jobPath%\photo_album_79.results
call getResults -successfile %jobPath%\photo_album_80.input.success -outputfile  %jobPath%\photo_album_80.results

PAUSE