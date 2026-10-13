@echo off
title ctf toolkit
cd /d "%~dp0"
python recon.py
if errorlevel 1 (
    echo.
    echo [!] script exited with an error. press any key to close.
    pause >nul
)