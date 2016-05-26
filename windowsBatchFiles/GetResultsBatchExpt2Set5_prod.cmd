@echo off
REM Windows batch file to get results on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call getResults -successfile %jobPath%\photo_album_41.input.success -outputfile  %jobPath%\photo_album_41.results
call getResults -successfile %jobPath%\photo_album_42.input.success -outputfile  %jobPath%\photo_album_42.results
call getResults -successfile %jobPath%\photo_album_43.input.success -outputfile  %jobPath%\photo_album_43.results
call getResults -successfile %jobPath%\photo_album_44.input.success -outputfile  %jobPath%\photo_album_44.results
call getResults -successfile %jobPath%\photo_album_45.input.success -outputfile  %jobPath%\photo_album_45.results
call getResults -successfile %jobPath%\photo_album_46.input.success -outputfile  %jobPath%\photo_album_46.results
call getResults -successfile %jobPath%\photo_album_47.input.success -outputfile  %jobPath%\photo_album_47.results
call getResults -successfile %jobPath%\photo_album_48.input.success -outputfile  %jobPath%\photo_album_48.results
call getResults -successfile %jobPath%\photo_album_49.input.success -outputfile  %jobPath%\photo_album_49.results
call getResults -successfile %jobPath%\photo_album_50.input.success -outputfile  %jobPath%\photo_album_50.results

PAUSE