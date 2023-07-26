@echo off
cd /d %~dp0
set python_script=run.py
IF NOT EXIST %python_script% (
    echo %python_script% does not exist
    pause
    exit
)
python %python_script%
IF %ERRORLEVEL% NEQ 0 (
    echo An error occurred while running %python_script%
    pause
)
exit