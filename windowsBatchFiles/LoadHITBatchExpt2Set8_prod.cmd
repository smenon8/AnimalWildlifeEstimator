@echo off
set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_71.input -question  %jobPath%\photo_album_71_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_72.input -question  %jobPath%\photo_album_72_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_73.input -question  %jobPath%\photo_album_73_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_74.input -question  %jobPath%\photo_album_74_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_75.input -question  %jobPath%\photo_album_75_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_76.input -question  %jobPath%\photo_album_76_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_77.input -question  %jobPath%\photo_album_77_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_78.input -question  %jobPath%\photo_album_78_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_79.input -question  %jobPath%\photo_album_79_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_80.input -question  %jobPath%\photo_album_80_prod.question -properties %jobPath%\photo_album.properties