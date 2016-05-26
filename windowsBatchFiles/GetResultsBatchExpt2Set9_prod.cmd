@echo off
REM Windows batch file to get results on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call getResults -successfile %jobPath%\photo_album_81.input.success -outputfile  %jobPath%\photo_album_81.results
call getResults -successfile %jobPath%\photo_album_82.input.success -outputfile  %jobPath%\photo_album_82.results
call getResults -successfile %jobPath%\photo_album_83.input.success -outputfile  %jobPath%\photo_album_83.results
call getResults -successfile %jobPath%\photo_album_84.input.success -outputfile  %jobPath%\photo_album_84.results
call getResults -successfile %jobPath%\photo_album_85.input.success -outputfile  %jobPath%\photo_album_85.results
call getResults -successfile %jobPath%\photo_album_86.input.success -outputfile  %jobPath%\photo_album_86.results
call getResults -successfile %jobPath%\photo_album_87.input.success -outputfile  %jobPath%\photo_album_87.results
call getResults -successfile %jobPath%\photo_album_88.input.success -outputfile  %jobPath%\photo_album_88.results
call getResults -successfile %jobPath%\photo_album_89.input.success -outputfile  %jobPath%\photo_album_89.results
call getResults -successfile %jobPath%\photo_album_90.input.success -outputfile  %jobPath%\photo_album_90.results

PAUSE