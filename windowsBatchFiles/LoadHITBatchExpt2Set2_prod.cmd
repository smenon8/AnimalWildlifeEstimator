@echo off
set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_11.input -question  %jobPath%\photo_album_11_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_12.input -question  %jobPath%\photo_album_12_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_13.input -question  %jobPath%\photo_album_13_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_14.input -question  %jobPath%\photo_album_14_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_15.input -question  %jobPath%\photo_album_15_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_16.input -question  %jobPath%\photo_album_16_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_17.input -question  %jobPath%\photo_album_17_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_18.input -question  %jobPath%\photo_album_18_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_19.input -question  %jobPath%\photo_album_19_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_20.input -question  %jobPath%\photo_album_20_prod.question -properties %jobPath%\photo_album.properties