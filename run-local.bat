@echo off
cd /d "%~dp0"
python server.py
if errorlevel 1 (
  echo.
  echo Could not start SAG VCE. Make sure Python 3.10 or newer is installed.
  pause
)
