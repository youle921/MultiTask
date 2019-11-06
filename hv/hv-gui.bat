@echo off

set /p REF=<%~dp0\reference.csv
for %%i in (%*) do java -cp %~dp0\indicator.jar;%~dp0\args4j\args4j-2.0.21.jar mo.measure.Hypervolume -r %REF% -vv %%i > %%~pdni.metricHV2