@echo off
set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_41.input -question  %jobPath%\photo_album_41_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_42.input -question  %jobPath%\photo_album_42_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_43.input -question  %jobPath%\photo_album_43_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_44.input -question  %jobPath%\photo_album_44_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_45.input -question  %jobPath%\photo_album_45_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_46.input -question  %jobPath%\photo_album_46_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_47.input -question  %jobPath%\photo_album_47_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_48.input -question  %jobPath%\photo_album_48_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_49.input -question  %jobPath%\photo_album_49_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_50.input -question  %jobPath%\photo_album_50_prod.question -properties %jobPath%\photo_album.properties