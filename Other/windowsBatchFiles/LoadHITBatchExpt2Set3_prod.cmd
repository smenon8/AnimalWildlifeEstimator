@echo off
set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_21.input -question  %jobPath%\photo_album_21_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_22.input -question  %jobPath%\photo_album_22_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_23.input -question  %jobPath%\photo_album_23_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_24.input -question  %jobPath%\photo_album_24_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_25.input -question  %jobPath%\photo_album_25_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_26.input -question  %jobPath%\photo_album_26_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_27.input -question  %jobPath%\photo_album_27_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_28.input -question  %jobPath%\photo_album_28_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_29.input -question  %jobPath%\photo_album_29_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_30.input -question  %jobPath%\photo_album_30_prod.question -properties %jobPath%\photo_album.properties