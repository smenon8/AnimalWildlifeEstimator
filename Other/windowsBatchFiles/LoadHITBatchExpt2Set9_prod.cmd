@echo off
set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_81.input -question  %jobPath%\photo_album_81_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_82.input -question  %jobPath%\photo_album_82_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_83.input -question  %jobPath%\photo_album_83_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_84.input -question  %jobPath%\photo_album_84_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_85.input -question  %jobPath%\photo_album_85_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_86.input -question  %jobPath%\photo_album_86_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_87.input -question  %jobPath%\photo_album_87_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_88.input -question  %jobPath%\photo_album_88_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_89.input -question  %jobPath%\photo_album_89_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_90.input -question  %jobPath%\photo_album_90_prod.question -properties %jobPath%\photo_album.properties