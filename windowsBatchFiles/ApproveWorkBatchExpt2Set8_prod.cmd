@echo off
REM Windows batch file to approve work on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call approveWork -successfile %jobPath%\photo_album_71.input.success
call approveWork -successfile %jobPath%\photo_album_72.input.success
call approveWork -successfile %jobPath%\photo_album_73.input.success
call approveWork -successfile %jobPath%\photo_album_74.input.success
call approveWork -successfile %jobPath%\photo_album_75.input.success
call approveWork -successfile %jobPath%\photo_album_76.input.success
call approveWork -successfile %jobPath%\photo_album_77.input.success
call approveWork -successfile %jobPath%\photo_album_78.input.success
call approveWork -successfile %jobPath%\photo_album_79.input.success
call approveWork -successfile %jobPath%\photo_album_80.input.success

PAUSE