@echo off
REM Windows batch file to load job into AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 15th April 2016

REM : Python script for printing the job commands

REM for i in range(1,101):
    REM inputFL = "photo_album_" + str(i) + ".input"
    REM questionFL ="photo_album_" + str(i) + "_prod.question"
    REM cmd = "call loadHITs -input %jobPath%\\" + inputFL + " -question  %jobPath%\\" + questionFL + " -properties %jobPath%\photo_album.properties -sandbox"
    REM print(cmd)

set /p directory="Enter source drive : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%

PAUSE
 
set /p jobPath="Enter jobs directory path : "

call loadHITs -input %jobPath%\photo_album_1.input -question  %jobPath%\photo_album_1_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_2.input -question  %jobPath%\photo_album_2_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_3.input -question  %jobPath%\photo_album_3_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_4.input -question  %jobPath%\photo_album_4_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_5.input -question  %jobPath%\photo_album_5_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_6.input -question  %jobPath%\photo_album_6_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_7.input -question  %jobPath%\photo_album_7_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_8.input -question  %jobPath%\photo_album_8_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_9.input -question  %jobPath%\photo_album_9_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_10.input -question  %jobPath%\photo_album_10_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_11.input -question  %jobPath%\photo_album_11_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_12.input -question  %jobPath%\photo_album_12_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_13.input -question  %jobPath%\photo_album_13_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_14.input -question  %jobPath%\photo_album_14_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_15.input -question  %jobPath%\photo_album_15_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_16.input -question  %jobPath%\photo_album_16_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_17.input -question  %jobPath%\photo_album_17_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_18.input -question  %jobPath%\photo_album_18_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_19.input -question  %jobPath%\photo_album_19_prod.question -properties %jobPath%\photo_album.properties
call loadHITs -input %jobPath%\photo_album_20.input -question  %jobPath%\photo_album_20_prod.question -properties %jobPath%\photo_album.properties
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