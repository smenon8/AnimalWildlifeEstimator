@echo off
set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_31.input -question  %jobPath%\photo_album_31_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_32.input -question  %jobPath%\photo_album_32_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_33.input -question  %jobPath%\photo_album_33_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_34.input -question  %jobPath%\photo_album_34_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_35.input -question  %jobPath%\photo_album_35_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_36.input -question  %jobPath%\photo_album_36_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_37.input -question  %jobPath%\photo_album_37_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_38.input -question  %jobPath%\photo_album_38_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_39.input -question  %jobPath%\photo_album_39_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_40.input -question  %jobPath%\photo_album_40_prod.question -properties %jobPath%\photo_album.properties