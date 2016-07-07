@echo off
set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_51.input -question  %jobPath%\photo_album_51_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_52.input -question  %jobPath%\photo_album_52_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_53.input -question  %jobPath%\photo_album_53_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_54.input -question  %jobPath%\photo_album_54_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_55.input -question  %jobPath%\photo_album_55_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_56.input -question  %jobPath%\photo_album_56_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_57.input -question  %jobPath%\photo_album_57_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_58.input -question  %jobPath%\photo_album_58_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_59.input -question  %jobPath%\photo_album_59_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_60.input -question  %jobPath%\photo_album_60_prod.question -properties %jobPath%\photo_album.properties