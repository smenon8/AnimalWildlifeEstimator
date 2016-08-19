@echo off
REM Windows batch file to approve work on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call approveWork -successfile %jobPath%\photo_album_81.input.success
call approveWork -successfile %jobPath%\photo_album_82.input.success
call approveWork -successfile %jobPath%\photo_album_83.input.success
call approveWork -successfile %jobPath%\photo_album_84.input.success
call approveWork -successfile %jobPath%\photo_album_85.input.success
call approveWork -successfile %jobPath%\photo_album_86.input.success
call approveWork -successfile %jobPath%\photo_album_87.input.success
call approveWork -successfile %jobPath%\photo_album_88.input.success
call approveWork -successfile %jobPath%\photo_album_89.input.success
call approveWork -successfile %jobPath%\photo_album_90.input.success

PAUSE