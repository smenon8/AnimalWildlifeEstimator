@echo off
set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_91.input -question  %jobPath%\photo_album_91_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_92.input -question  %jobPath%\photo_album_92_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_93.input -question  %jobPath%\photo_album_93_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_94.input -question  %jobPath%\photo_album_94_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_95.input -question  %jobPath%\photo_album_95_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_96.input -question  %jobPath%\photo_album_96_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_97.input -question  %jobPath%\photo_album_97_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_98.input -question  %jobPath%\photo_album_98_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_99.input -question  %jobPath%\photo_album_99_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_100.input -question  %jobPath%\photo_album_100_prod.question -properties %jobPath%\photo_album.properties