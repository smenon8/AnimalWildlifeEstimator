@echo off
REM Windows batch file to approve work on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call approveWork -successfile %jobPath%\photo_album_91.input.success
call approveWork -successfile %jobPath%\photo_album_92.input.success
call approveWork -successfile %jobPath%\photo_album_93.input.success
call approveWork -successfile %jobPath%\photo_album_94.input.success
call approveWork -successfile %jobPath%\photo_album_95.input.success
call approveWork -successfile %jobPath%\photo_album_96.input.success
call approveWork -successfile %jobPath%\photo_album_97.input.success
call approveWork -successfile %jobPath%\photo_album_98.input.success
call approveWork -successfile %jobPath%\photo_album_99.input.success
call approveWork -successfile %jobPath%\photo_album_100.input.success

PAUSE