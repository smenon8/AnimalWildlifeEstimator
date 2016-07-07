@echo off
set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_61.input -question  %jobPath%\photo_album_61_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_62.input -question  %jobPath%\photo_album_62_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_63.input -question  %jobPath%\photo_album_63_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_64.input -question  %jobPath%\photo_album_64_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_65.input -question  %jobPath%\photo_album_65_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_66.input -question  %jobPath%\photo_album_66_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_67.input -question  %jobPath%\photo_album_67_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_68.input -question  %jobPath%\photo_album_68_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_69.input -question  %jobPath%\photo_album_69_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_70.input -question  %jobPath%\photo_album_70_prod.question -properties %jobPath%\photo_album.properties