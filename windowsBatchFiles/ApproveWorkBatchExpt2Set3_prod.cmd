@echo off
REM Windows batch file to approve work on the basis of success files from AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 21th May 2016

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call approveWork -successfile %jobPath%\photo_album_21.input.success
call approveWork -successfile %jobPath%\photo_album_22.input.success
call approveWork -successfile %jobPath%\photo_album_23.input.success
call approveWork -successfile %jobPath%\photo_album_24.input.success
call approveWork -successfile %jobPath%\photo_album_25.input.success
call approveWork -successfile %jobPath%\photo_album_26.input.success
call approveWork -successfile %jobPath%\photo_album_27.input.success
call approveWork -successfile %jobPath%\photo_album_28.input.success
call approveWork -successfile %jobPath%\photo_album_29.input.success
call approveWork -successfile %jobPath%\photo_album_30.input.success

PAUSE