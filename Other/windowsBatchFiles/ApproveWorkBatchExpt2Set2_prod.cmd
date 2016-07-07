@echo off
REM Windows batch file to approve work on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call approveWork -successfile %jobPath%\photo_album_11.input.success
call approveWork -successfile %jobPath%\photo_album_12.input.success
call approveWork -successfile %jobPath%\photo_album_13.input.success
call approveWork -successfile %jobPath%\photo_album_14.input.success
call approveWork -successfile %jobPath%\photo_album_15.input.success
call approveWork -successfile %jobPath%\photo_album_16.input.success
call approveWork -successfile %jobPath%\photo_album_17.input.success
call approveWork -successfile %jobPath%\photo_album_18.input.success
call approveWork -successfile %jobPath%\photo_album_19.input.success
call approveWork -successfile %jobPath%\photo_album_20.input.success

PAUSE