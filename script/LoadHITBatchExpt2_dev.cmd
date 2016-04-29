REM Windows batch file to load job into AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 15th April 2016

REM : Python script for printing the job commands

REM for i in range(1,101):
    REM inputFL = "photo_album_" + str(i) + ".input"
    REM questionFL ="photo_album_" + str(i) + ".question"
    REM cmd = "call loadHITs -input %jobPath%\\" + inputFL + " -question  %jobPath%\\" + questionFL + " -properties %jobPath%\photo_album.properties -sandbox"
    REM print(cmd)

@echo off
set /p directory="Enter source directory : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

PAUSE
 
set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_1.input -question  %jobPath%\photo_album_1.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_2.input -question  %jobPath%\photo_album_2.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_3.input -question  %jobPath%\photo_album_3.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_4.input -question  %jobPath%\photo_album_4.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_5.input -question  %jobPath%\photo_album_5.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_6.input -question  %jobPath%\photo_album_6.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_7.input -question  %jobPath%\photo_album_7.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_8.input -question  %jobPath%\photo_album_8.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_9.input -question  %jobPath%\photo_album_9.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_10.input -question  %jobPath%\photo_album_10.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_11.input -question  %jobPath%\photo_album_11.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_12.input -question  %jobPath%\photo_album_12.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_13.input -question  %jobPath%\photo_album_13.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_14.input -question  %jobPath%\photo_album_14.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_15.input -question  %jobPath%\photo_album_15.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_16.input -question  %jobPath%\photo_album_16.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_17.input -question  %jobPath%\photo_album_17.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_18.input -question  %jobPath%\photo_album_18.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_19.input -question  %jobPath%\photo_album_19.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_20.input -question  %jobPath%\photo_album_20.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_21.input -question  %jobPath%\photo_album_21.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_22.input -question  %jobPath%\photo_album_22.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_23.input -question  %jobPath%\photo_album_23.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_24.input -question  %jobPath%\photo_album_24.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_25.input -question  %jobPath%\photo_album_25.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_26.input -question  %jobPath%\photo_album_26.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_27.input -question  %jobPath%\photo_album_27.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_28.input -question  %jobPath%\photo_album_28.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_29.input -question  %jobPath%\photo_album_29.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_30.input -question  %jobPath%\photo_album_30.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_31.input -question  %jobPath%\photo_album_31.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_32.input -question  %jobPath%\photo_album_32.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_33.input -question  %jobPath%\photo_album_33.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_34.input -question  %jobPath%\photo_album_34.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_35.input -question  %jobPath%\photo_album_35.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_36.input -question  %jobPath%\photo_album_36.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_37.input -question  %jobPath%\photo_album_37.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_38.input -question  %jobPath%\photo_album_38.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_39.input -question  %jobPath%\photo_album_39.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_40.input -question  %jobPath%\photo_album_40.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_41.input -question  %jobPath%\photo_album_41.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_42.input -question  %jobPath%\photo_album_42.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_43.input -question  %jobPath%\photo_album_43.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_44.input -question  %jobPath%\photo_album_44.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_45.input -question  %jobPath%\photo_album_45.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_46.input -question  %jobPath%\photo_album_46.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_47.input -question  %jobPath%\photo_album_47.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_48.input -question  %jobPath%\photo_album_48.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_49.input -question  %jobPath%\photo_album_49.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_50.input -question  %jobPath%\photo_album_50.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_51.input -question  %jobPath%\photo_album_51.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_52.input -question  %jobPath%\photo_album_52.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_53.input -question  %jobPath%\photo_album_53.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_54.input -question  %jobPath%\photo_album_54.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_55.input -question  %jobPath%\photo_album_55.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_56.input -question  %jobPath%\photo_album_56.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_57.input -question  %jobPath%\photo_album_57.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_58.input -question  %jobPath%\photo_album_58.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_59.input -question  %jobPath%\photo_album_59.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_60.input -question  %jobPath%\photo_album_60.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_61.input -question  %jobPath%\photo_album_61.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_62.input -question  %jobPath%\photo_album_62.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_63.input -question  %jobPath%\photo_album_63.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_64.input -question  %jobPath%\photo_album_64.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_65.input -question  %jobPath%\photo_album_65.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_66.input -question  %jobPath%\photo_album_66.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_67.input -question  %jobPath%\photo_album_67.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_68.input -question  %jobPath%\photo_album_68.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_69.input -question  %jobPath%\photo_album_69.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_70.input -question  %jobPath%\photo_album_70.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_71.input -question  %jobPath%\photo_album_71.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_72.input -question  %jobPath%\photo_album_72.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_73.input -question  %jobPath%\photo_album_73.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_74.input -question  %jobPath%\photo_album_74.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_75.input -question  %jobPath%\photo_album_75.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_76.input -question  %jobPath%\photo_album_76.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_77.input -question  %jobPath%\photo_album_77.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_78.input -question  %jobPath%\photo_album_78.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_79.input -question  %jobPath%\photo_album_79.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_80.input -question  %jobPath%\photo_album_80.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_81.input -question  %jobPath%\photo_album_81.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_82.input -question  %jobPath%\photo_album_82.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_83.input -question  %jobPath%\photo_album_83.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_84.input -question  %jobPath%\photo_album_84.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_85.input -question  %jobPath%\photo_album_85.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_86.input -question  %jobPath%\photo_album_86.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_87.input -question  %jobPath%\photo_album_87.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_88.input -question  %jobPath%\photo_album_88.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_89.input -question  %jobPath%\photo_album_89.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_90.input -question  %jobPath%\photo_album_90.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_91.input -question  %jobPath%\photo_album_91.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_92.input -question  %jobPath%\photo_album_92.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_93.input -question  %jobPath%\photo_album_93.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_94.input -question  %jobPath%\photo_album_94.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_95.input -question  %jobPath%\photo_album_95.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_96.input -question  %jobPath%\photo_album_96.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_97.input -question  %jobPath%\photo_album_97.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_98.input -question  %jobPath%\photo_album_98.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_99.input -question  %jobPath%\photo_album_99.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\photo_album_100.input -question  %jobPath%\photo_album_100.question -properties %jobPath%\photo_album.properties -sandbox
PAUSE