@echo off
REM Windows batch file to get results on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call getResults -successfile %jobPath%\photo_album_91.input.success -outputfile  %jobPath%\photo_album_91.results
call getResults -successfile %jobPath%\photo_album_92.input.success -outputfile  %jobPath%\photo_album_92.results
call getResults -successfile %jobPath%\photo_album_93.input.success -outputfile  %jobPath%\photo_album_93.results
call getResults -successfile %jobPath%\photo_album_94.input.success -outputfile  %jobPath%\photo_album_94.results
call getResults -successfile %jobPath%\photo_album_95.input.success -outputfile  %jobPath%\photo_album_95.results
call getResults -successfile %jobPath%\photo_album_96.input.success -outputfile  %jobPath%\photo_album_96.results
call getResults -successfile %jobPath%\photo_album_97.input.success -outputfile  %jobPath%\photo_album_97.results
call getResults -successfile %jobPath%\photo_album_98.input.success -outputfile  %jobPath%\photo_album_98.results
call getResults -successfile %jobPath%\photo_album_99.input.success -outputfile  %jobPath%\photo_album_99.results
call getResults -successfile %jobPath%\photo_album_100.input.success -outputfile  %jobPath%\photo_album_100.results

PAUSE