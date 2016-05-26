@echo off
REM Windows batch file to approve work on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call approveWork -successfile %jobPath%\photo_album_51.input.success
call approveWork -successfile %jobPath%\photo_album_52.input.success
call approveWork -successfile %jobPath%\photo_album_53.input.success
call approveWork -successfile %jobPath%\photo_album_54.input.success
call approveWork -successfile %jobPath%\photo_album_55.input.success
call approveWork -successfile %jobPath%\photo_album_56.input.success
call approveWork -successfile %jobPath%\photo_album_57.input.success
call approveWork -successfile %jobPath%\photo_album_58.input.success
call approveWork -successfile %jobPath%\photo_album_59.input.success
call approveWork -successfile %jobPath%\photo_album_60.input.success

PAUSE