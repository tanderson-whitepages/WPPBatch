@ECHO OFF
REM This script simply provides a way to drag-and-drop an input file to pass it to the python script below.
REM See that python script for further details
python "%~dp0/scripts/SearchAddressIntelligence.py" "%~1"
set /p foo=Hit enter to quit