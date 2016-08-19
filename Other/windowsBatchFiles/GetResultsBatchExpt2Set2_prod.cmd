@echo off
REM Windows batch file to get results on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call getResults -successfile %jobPath%\photo_album_11.input.success -outputfile  %jobPath%\photo_album_11.results
call getResults -successfile %jobPath%\photo_album_12.input.success -outputfile  %jobPath%\photo_album_12.results
call getResults -successfile %jobPath%\photo_album_13.input.success -outputfile  %jobPath%\photo_album_13.results
call getResults -successfile %jobPath%\photo_album_14.input.success -outputfile  %jobPath%\photo_album_14.results
call getResults -successfile %jobPath%\photo_album_15.input.success -outputfile  %jobPath%\photo_album_15.results
call getResults -successfile %jobPath%\photo_album_16.input.success -outputfile  %jobPath%\photo_album_16.results
call getResults -successfile %jobPath%\photo_album_17.input.success -outputfile  %jobPath%\photo_album_17.results
call getResults -successfile %jobPath%\photo_album_18.input.success -outputfile  %jobPath%\photo_album_18.results
call getResults -successfile %jobPath%\photo_album_19.input.success -outputfile  %jobPath%\photo_album_19.results
call getResults -successfile %jobPath%\photo_album_20.input.success -outputfile  %jobPath%\photo_album_20.results

PAUSE
