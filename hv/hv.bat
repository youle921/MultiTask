@echo off

java -cp %~dp0\indicator.jar;%~dp0\args4j\args4j-2.0.21.jar mo.measure.Hypervolume %*

pause