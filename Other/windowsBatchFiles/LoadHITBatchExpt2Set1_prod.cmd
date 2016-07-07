@echo off
set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_1.input -question  %jobPath%\photo_album_1_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_2.input -question  %jobPath%\photo_album_2_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_3.input -question  %jobPath%\photo_album_3_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_4.input -question  %jobPath%\photo_album_4_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_5.input -question  %jobPath%\photo_album_5_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_6.input -question  %jobPath%\photo_album_6_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_7.input -question  %jobPath%\photo_album_7_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_8.input -question  %jobPath%\photo_album_8_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_9.input -question  %jobPath%\photo_album_9_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_10.input -question  %jobPath%\photo_album_10_prod.question -properties %jobPath%\photo_album.properties