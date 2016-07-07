@echo off
REM Windows batch file to approve work on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call approveWork -successfile %jobPath%\photo_album_41.input.success
call approveWork -successfile %jobPath%\photo_album_42.input.success
call approveWork -successfile %jobPath%\photo_album_43.input.success
call approveWork -successfile %jobPath%\photo_album_44.input.success
call approveWork -successfile %jobPath%\photo_album_45.input.success
call approveWork -successfile %jobPath%\photo_album_46.input.success
call approveWork -successfile %jobPath%\photo_album_47.input.success
call approveWork -successfile %jobPath%\photo_album_48.input.success
call approveWork -successfile %jobPath%\photo_album_49.input.success
call approveWork -successfile %jobPath%\photo_album_50.input.success

PAUSE