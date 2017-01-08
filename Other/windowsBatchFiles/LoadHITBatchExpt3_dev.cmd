@echo off

REM Windows batch file to load job into AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 15th April 2016

REM : Python script for printing the job commands

REM for i in range(1,101):
    REM inputFL = "photo_album_" + str(i) + ".input"
    REM questionFL ="photo_album_" + str(i) + ".question"
    REM cmd = "call loadHITs -input %jobPath%\\" + inputFL + " -question  %jobPath%\\" + questionFL + " -properties %jobPath%\photo_album.properties -sandbox"
    REM print(cmd)


set /p directory="Enter source directory : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%
 
set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\Expt3_1.input -question  %jobPath%\Expt3_1.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_2.input -question  %jobPath%\Expt3_2.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_3.input -question  %jobPath%\Expt3_3.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_4.input -question  %jobPath%\Expt3_4.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_5.input -question  %jobPath%\Expt3_5.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_6.input -question  %jobPath%\Expt3_6.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_7.input -question  %jobPath%\Expt3_7.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_8.input -question  %jobPath%\Expt3_8.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_9.input -question  %jobPath%\Expt3_9.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_10.input -question  %jobPath%\Expt3_10.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_11.input -question  %jobPath%\Expt3_11.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_12.input -question  %jobPath%\Expt3_12.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_13.input -question  %jobPath%\Expt3_13.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_14.input -question  %jobPath%\Expt3_14.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_15.input -question  %jobPath%\Expt3_15.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_16.input -question  %jobPath%\Expt3_16.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_17.input -question  %jobPath%\Expt3_17.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_18.input -question  %jobPath%\Expt3_18.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_19.input -question  %jobPath%\Expt3_19.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_20.input -question  %jobPath%\Expt3_20.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_21.input -question  %jobPath%\Expt3_21.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_22.input -question  %jobPath%\Expt3_22.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_23.input -question  %jobPath%\Expt3_23.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_24.input -question  %jobPath%\Expt3_24.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_25.input -question  %jobPath%\Expt3_25.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_26.input -question  %jobPath%\Expt3_26.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_27.input -question  %jobPath%\Expt3_27.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_28.input -question  %jobPath%\Expt3_28.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_29.input -question  %jobPath%\Expt3_29.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_30.input -question  %jobPath%\Expt3_30.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_31.input -question  %jobPath%\Expt3_31.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_32.input -question  %jobPath%\Expt3_32.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_33.input -question  %jobPath%\Expt3_33.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_34.input -question  %jobPath%\Expt3_34.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_35.input -question  %jobPath%\Expt3_35.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_36.input -question  %jobPath%\Expt3_36.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_37.input -question  %jobPath%\Expt3_37.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_38.input -question  %jobPath%\Expt3_38.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_39.input -question  %jobPath%\Expt3_39.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_40.input -question  %jobPath%\Expt3_40.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_41.input -question  %jobPath%\Expt3_41.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_42.input -question  %jobPath%\Expt3_42.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_43.input -question  %jobPath%\Expt3_43.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_44.input -question  %jobPath%\Expt3_44.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_45.input -question  %jobPath%\Expt3_45.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_46.input -question  %jobPath%\Expt3_46.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_47.input -question  %jobPath%\Expt3_47.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_48.input -question  %jobPath%\Expt3_48.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_49.input -question  %jobPath%\Expt3_49.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_50.input -question  %jobPath%\Expt3_50.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_51.input -question  %jobPath%\Expt3_51.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_52.input -question  %jobPath%\Expt3_52.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_53.input -question  %jobPath%\Expt3_53.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_54.input -question  %jobPath%\Expt3_54.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_55.input -question  %jobPath%\Expt3_55.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_56.input -question  %jobPath%\Expt3_56.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_57.input -question  %jobPath%\Expt3_57.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_58.input -question  %jobPath%\Expt3_58.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_59.input -question  %jobPath%\Expt3_59.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_60.input -question  %jobPath%\Expt3_60.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_61.input -question  %jobPath%\Expt3_61.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_62.input -question  %jobPath%\Expt3_62.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_63.input -question  %jobPath%\Expt3_63.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_64.input -question  %jobPath%\Expt3_64.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_65.input -question  %jobPath%\Expt3_65.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_66.input -question  %jobPath%\Expt3_66.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_67.input -question  %jobPath%\Expt3_67.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_68.input -question  %jobPath%\Expt3_68.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_69.input -question  %jobPath%\Expt3_69.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_70.input -question  %jobPath%\Expt3_70.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_71.input -question  %jobPath%\Expt3_71.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_72.input -question  %jobPath%\Expt3_72.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_73.input -question  %jobPath%\Expt3_73.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_74.input -question  %jobPath%\Expt3_74.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_75.input -question  %jobPath%\Expt3_75.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_76.input -question  %jobPath%\Expt3_76.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_77.input -question  %jobPath%\Expt3_77.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_78.input -question  %jobPath%\Expt3_78.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_79.input -question  %jobPath%\Expt3_79.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_80.input -question  %jobPath%\Expt3_80.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_81.input -question  %jobPath%\Expt3_81.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_82.input -question  %jobPath%\Expt3_82.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_83.input -question  %jobPath%\Expt3_83.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_84.input -question  %jobPath%\Expt3_84.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_85.input -question  %jobPath%\Expt3_85.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_86.input -question  %jobPath%\Expt3_86.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_87.input -question  %jobPath%\Expt3_87.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_88.input -question  %jobPath%\Expt3_88.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_89.input -question  %jobPath%\Expt3_89.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_90.input -question  %jobPath%\Expt3_90.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_91.input -question  %jobPath%\Expt3_91.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_92.input -question  %jobPath%\Expt3_92.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_93.input -question  %jobPath%\Expt3_93.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_94.input -question  %jobPath%\Expt3_94.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_95.input -question  %jobPath%\Expt3_95.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_96.input -question  %jobPath%\Expt3_96.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_97.input -question  %jobPath%\Expt3_97.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_98.input -question  %jobPath%\Expt3_98.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_99.input -question  %jobPath%\Expt3_99.question -properties %jobPath%\photo_album.properties -sandbox
call loadHITs -input %jobPath%\Expt3_100.input -question  %jobPath%\Expt3_100.question -properties %jobPath%\photo_album.properties -sandbox

PAUSE