@echo off
REM Windows batch file to get results on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call getResults -successfile %jobPath%\photo_album_61.input.success -outputfile  %jobPath%\photo_album_61.results
call getResults -successfile %jobPath%\photo_album_62.input.success -outputfile  %jobPath%\photo_album_62.results
call getResults -successfile %jobPath%\photo_album_63.input.success -outputfile  %jobPath%\photo_album_63.results
call getResults -successfile %jobPath%\photo_album_64.input.success -outputfile  %jobPath%\photo_album_64.results
call getResults -successfile %jobPath%\photo_album_65.input.success -outputfile  %jobPath%\photo_album_65.results
call getResults -successfile %jobPath%\photo_album_66.input.success -outputfile  %jobPath%\photo_album_66.results
call getResults -successfile %jobPath%\photo_album_67.input.success -outputfile  %jobPath%\photo_album_67.results
call getResults -successfile %jobPath%\photo_album_68.input.success -outputfile  %jobPath%\photo_album_68.results
call getResults -successfile %jobPath%\photo_album_69.input.success -outputfile  %jobPath%\photo_album_69.results
call getResults -successfile %jobPath%\photo_album_70.input.success -outputfile  %jobPath%\photo_album_70.results

PAUSE