@echo off
REM Windows batch file to approve work on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call approveWork -successfile %jobPath%\photo_album_31.input.success
call approveWork -successfile %jobPath%\photo_album_32.input.success
call approveWork -successfile %jobPath%\photo_album_33.input.success
call approveWork -successfile %jobPath%\photo_album_34.input.success
call approveWork -successfile %jobPath%\photo_album_35.input.success
call approveWork -successfile %jobPath%\photo_album_36.input.success
call approveWork -successfile %jobPath%\photo_album_37.input.success
call approveWork -successfile %jobPath%\photo_album_38.input.success
call approveWork -successfile %jobPath%\photo_album_39.input.success
call approveWork -successfile %jobPath%\photo_album_40.input.success

PAUSE