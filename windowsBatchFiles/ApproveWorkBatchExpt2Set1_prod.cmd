@echo off
REM Windows batch file to approve work on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call approveWork -successfile %jobPath%\photo_album_1.input.success
call approveWork -successfile %jobPath%\photo_album_2.input.success
call approveWork -successfile %jobPath%\photo_album_3.input.success
call approveWork -successfile %jobPath%\photo_album_4.input.success
call approveWork -successfile %jobPath%\photo_album_5.input.success
call approveWork -successfile %jobPath%\photo_album_6.input.success
call approveWork -successfile %jobPath%\photo_album_7.input.success
call approveWork -successfile %jobPath%\photo_album_8.input.success
call approveWork -successfile %jobPath%\photo_album_9.input.success
call approveWork -successfile %jobPath%\photo_album_10.input.success

PAUSE