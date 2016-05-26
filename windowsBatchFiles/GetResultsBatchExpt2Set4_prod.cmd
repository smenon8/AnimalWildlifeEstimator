@echo off
REM Windows batch file to get results on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call getResults -successfile %jobPath%\photo_album_31.input.success -outputfile  %jobPath%\photo_album_31.results
call getResults -successfile %jobPath%\photo_album_32.input.success -outputfile  %jobPath%\photo_album_32.results
call getResults -successfile %jobPath%\photo_album_33.input.success -outputfile  %jobPath%\photo_album_33.results
call getResults -successfile %jobPath%\photo_album_34.input.success -outputfile  %jobPath%\photo_album_34.results
call getResults -successfile %jobPath%\photo_album_35.input.success -outputfile  %jobPath%\photo_album_35.results
call getResults -successfile %jobPath%\photo_album_36.input.success -outputfile  %jobPath%\photo_album_36.results
call getResults -successfile %jobPath%\photo_album_37.input.success -outputfile  %jobPath%\photo_album_37.results
call getResults -successfile %jobPath%\photo_album_38.input.success -outputfile  %jobPath%\photo_album_38.results
call getResults -successfile %jobPath%\photo_album_39.input.success -outputfile  %jobPath%\photo_album_39.results
call getResults -successfile %jobPath%\photo_album_40.input.success -outputfile  %jobPath%\photo_album_40.results

PAUSE