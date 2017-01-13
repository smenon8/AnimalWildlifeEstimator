@echo off

REM Windows batch file to load job into AWS Mechanical Turk
REM Author: Sreejith Menon
REM Date: 15th April 2016

set /p directory="Enter source directory : "
%directory%:

set /p mTurkPath="Enter AWS CLT bin directory path : "
cd %mTurkPath%
 
set /p jobPath="Enter jobs directory path : "

call ​getResults -successfile %jobPath%\Expt3_photo_album_1.input.success -outputfile  %jobPath%\Expt3_photo_album_1.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_2.input.success -outputfile  %jobPath%\Expt3_photo_album_2.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_3.input.success -outputfile  %jobPath%\Expt3_photo_album_3.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_4.input.success -outputfile  %jobPath%\Expt3_photo_album_4.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_5.input.success -outputfile  %jobPath%\Expt3_photo_album_5.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_6.input.success -outputfile  %jobPath%\Expt3_photo_album_6.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_7.input.success -outputfile  %jobPath%\Expt3_photo_album_7.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_8.input.success -outputfile  %jobPath%\Expt3_photo_album_8.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_9.input.success -outputfile  %jobPath%\Expt3_photo_album_9.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_10.input.success -outputfile  %jobPath%\Expt3_photo_album_10.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_11.input.success -outputfile  %jobPath%\Expt3_photo_album_11.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_12.input.success -outputfile  %jobPath%\Expt3_photo_album_12.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_13.input.success -outputfile  %jobPath%\Expt3_photo_album_13.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_14.input.success -outputfile  %jobPath%\Expt3_photo_album_14.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_15.input.success -outputfile  %jobPath%\Expt3_photo_album_15.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_16.input.success -outputfile  %jobPath%\Expt3_photo_album_16.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_17.input.success -outputfile  %jobPath%\Expt3_photo_album_17.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_18.input.success -outputfile  %jobPath%\Expt3_photo_album_18.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_19.input.success -outputfile  %jobPath%\Expt3_photo_album_19.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_20.input.success -outputfile  %jobPath%\Expt3_photo_album_20.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_21.input.success -outputfile  %jobPath%\Expt3_photo_album_21.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_22.input.success -outputfile  %jobPath%\Expt3_photo_album_22.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_23.input.success -outputfile  %jobPath%\Expt3_photo_album_23.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_24.input.success -outputfile  %jobPath%\Expt3_photo_album_24.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_25.input.success -outputfile  %jobPath%\Expt3_photo_album_25.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_26.input.success -outputfile  %jobPath%\Expt3_photo_album_26.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_27.input.success -outputfile  %jobPath%\Expt3_photo_album_27.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_28.input.success -outputfile  %jobPath%\Expt3_photo_album_28.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_29.input.success -outputfile  %jobPath%\Expt3_photo_album_29.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_30.input.success -outputfile  %jobPath%\Expt3_photo_album_30.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_31.input.success -outputfile  %jobPath%\Expt3_photo_album_31.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_32.input.success -outputfile  %jobPath%\Expt3_photo_album_32.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_33.input.success -outputfile  %jobPath%\Expt3_photo_album_33.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_34.input.success -outputfile  %jobPath%\Expt3_photo_album_34.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_35.input.success -outputfile  %jobPath%\Expt3_photo_album_35.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_36.input.success -outputfile  %jobPath%\Expt3_photo_album_36.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_37.input.success -outputfile  %jobPath%\Expt3_photo_album_37.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_38.input.success -outputfile  %jobPath%\Expt3_photo_album_38.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_39.input.success -outputfile  %jobPath%\Expt3_photo_album_39.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_40.input.success -outputfile  %jobPath%\Expt3_photo_album_40.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_41.input.success -outputfile  %jobPath%\Expt3_photo_album_41.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_42.input.success -outputfile  %jobPath%\Expt3_photo_album_42.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_43.input.success -outputfile  %jobPath%\Expt3_photo_album_43.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_44.input.success -outputfile  %jobPath%\Expt3_photo_album_44.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_45.input.success -outputfile  %jobPath%\Expt3_photo_album_45.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_46.input.success -outputfile  %jobPath%\Expt3_photo_album_46.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_47.input.success -outputfile  %jobPath%\Expt3_photo_album_47.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_48.input.success -outputfile  %jobPath%\Expt3_photo_album_48.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_49.input.success -outputfile  %jobPath%\Expt3_photo_album_49.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_50.input.success -outputfile  %jobPath%\Expt3_photo_album_50.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_51.input.success -outputfile  %jobPath%\Expt3_photo_album_51.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_52.input.success -outputfile  %jobPath%\Expt3_photo_album_52.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_53.input.success -outputfile  %jobPath%\Expt3_photo_album_53.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_54.input.success -outputfile  %jobPath%\Expt3_photo_album_54.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_55.input.success -outputfile  %jobPath%\Expt3_photo_album_55.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_56.input.success -outputfile  %jobPath%\Expt3_photo_album_56.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_57.input.success -outputfile  %jobPath%\Expt3_photo_album_57.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_58.input.success -outputfile  %jobPath%\Expt3_photo_album_58.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_59.input.success -outputfile  %jobPath%\Expt3_photo_album_59.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_60.input.success -outputfile  %jobPath%\Expt3_photo_album_60.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_61.input.success -outputfile  %jobPath%\Expt3_photo_album_61.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_62.input.success -outputfile  %jobPath%\Expt3_photo_album_62.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_63.input.success -outputfile  %jobPath%\Expt3_photo_album_63.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_64.input.success -outputfile  %jobPath%\Expt3_photo_album_64.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_65.input.success -outputfile  %jobPath%\Expt3_photo_album_65.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_66.input.success -outputfile  %jobPath%\Expt3_photo_album_66.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_67.input.success -outputfile  %jobPath%\Expt3_photo_album_67.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_68.input.success -outputfile  %jobPath%\Expt3_photo_album_68.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_69.input.success -outputfile  %jobPath%\Expt3_photo_album_69.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_70.input.success -outputfile  %jobPath%\Expt3_photo_album_70.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_71.input.success -outputfile  %jobPath%\Expt3_photo_album_71.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_72.input.success -outputfile  %jobPath%\Expt3_photo_album_72.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_73.input.success -outputfile  %jobPath%\Expt3_photo_album_73.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_74.input.success -outputfile  %jobPath%\Expt3_photo_album_74.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_75.input.success -outputfile  %jobPath%\Expt3_photo_album_75.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_76.input.success -outputfile  %jobPath%\Expt3_photo_album_76.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_77.input.success -outputfile  %jobPath%\Expt3_photo_album_77.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_78.input.success -outputfile  %jobPath%\Expt3_photo_album_78.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_79.input.success -outputfile  %jobPath%\Expt3_photo_album_79.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_80.input.success -outputfile  %jobPath%\Expt3_photo_album_80.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_81.input.success -outputfile  %jobPath%\Expt3_photo_album_81.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_82.input.success -outputfile  %jobPath%\Expt3_photo_album_82.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_83.input.success -outputfile  %jobPath%\Expt3_photo_album_83.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_84.input.success -outputfile  %jobPath%\Expt3_photo_album_84.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_85.input.success -outputfile  %jobPath%\Expt3_photo_album_85.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_86.input.success -outputfile  %jobPath%\Expt3_photo_album_86.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_87.input.success -outputfile  %jobPath%\Expt3_photo_album_87.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_88.input.success -outputfile  %jobPath%\Expt3_photo_album_88.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_89.input.success -outputfile  %jobPath%\Expt3_photo_album_89.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_90.input.success -outputfile  %jobPath%\Expt3_photo_album_90.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_91.input.success -outputfile  %jobPath%\Expt3_photo_album_91.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_92.input.success -outputfile  %jobPath%\Expt3_photo_album_92.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_93.input.success -outputfile  %jobPath%\Expt3_photo_album_93.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_94.input.success -outputfile  %jobPath%\Expt3_photo_album_94.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_95.input.success -outputfile  %jobPath%\Expt3_photo_album_95.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_96.input.success -outputfile  %jobPath%\Expt3_photo_album_96.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_97.input.success -outputfile  %jobPath%\Expt3_photo_album_97.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_98.input.success -outputfile  %jobPath%\Expt3_photo_album_98.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_99.input.success -outputfile  %jobPath%\Expt3_photo_album_99.results
call ​getResults -successfile %jobPath%\Expt3_photo_album_100.input.success -outputfile  %jobPath%\Expt3_photo_album_100.results

PAUSE