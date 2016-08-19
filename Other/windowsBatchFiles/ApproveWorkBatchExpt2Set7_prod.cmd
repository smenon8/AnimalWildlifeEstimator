@echo off
REM Windows batch file to approve work on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call approveWork -successfile %jobPath%\photo_album_61.input.success
call approveWork -successfile %jobPath%\photo_album_62.input.success
call approveWork -successfile %jobPath%\photo_album_63.input.success
call approveWork -successfile %jobPath%\photo_album_64.input.success
call approveWork -successfile %jobPath%\photo_album_65.input.success
call approveWork -successfile %jobPath%\photo_album_66.input.success
call approveWork -successfile %jobPath%\photo_album_67.input.success
call approveWork -successfile %jobPath%\photo_album_68.input.success
call approveWork -successfile %jobPath%\photo_album_69.input.success
call approveWork -successfile %jobPath%\photo_album_70.input.success

PAUSE