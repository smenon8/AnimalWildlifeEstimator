@echo off
REM Windows batch file to get results on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call getResults -successfile %jobPath%\photo_album_51.input.success -outputfile  %jobPath%\photo_album_51.results
call getResults -successfile %jobPath%\photo_album_52.input.success -outputfile  %jobPath%\photo_album_52.results
call getResults -successfile %jobPath%\photo_album_53.input.success -outputfile  %jobPath%\photo_album_53.results
call getResults -successfile %jobPath%\photo_album_54.input.success -outputfile  %jobPath%\photo_album_54.results
call getResults -successfile %jobPath%\photo_album_55.input.success -outputfile  %jobPath%\photo_album_55.results
call getResults -successfile %jobPath%\photo_album_56.input.success -outputfile  %jobPath%\photo_album_56.results
call getResults -successfile %jobPath%\photo_album_57.input.success -outputfile  %jobPath%\photo_album_57.results
call getResults -successfile %jobPath%\photo_album_58.input.success -outputfile  %jobPath%\photo_album_58.results
call getResults -successfile %jobPath%\photo_album_59.input.success -outputfile  %jobPath%\photo_album_59.results
call getResults -successfile %jobPath%\photo_album_60.input.success -outputfile  %jobPath%\photo_album_60.results

PAUSE