@echo off
title Test Environment

:: ============================================================
:: 1. DISPLAY WARNING MESSAGE
:: ============================================================
cls
echo ============================================================
echo           DO NOT CLOSE THIS WINDOW
echo ============================================================
echo This window is required to log errors and run the program.
echo Closing it will stop the application immediately.
echo ============================================================
echo.
echo Initializing environment...
echo.

:: 2. FIND ANACONDA ENVIRONMENT

if exist "C:\ProgramData\Anaconda3\Scripts\activate.bat" (
    set "ANACONDA_PATH=C:\ProgramData\Anaconda3"
) else if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
    set "ANACONDA_PATH=%USERPROFILE%\anaconda3"
) else (
    cls
    echo ============================================================
    echo    CRITICAL ERROR: CANNOT START THE TEST ON THIS DEVICE.
    echo ============================================================

    echo ERROR: The test cannot be executed on this device.
    echo.
    echo Please try a different device with Anaconda installed.
    echo.
    pause
    exit /b 1
)


:: Activate the base environment
call "%ANACONDA_PATH%\Scripts\activate.bat" "%ANACONDA_PATH%"

:: FIX: Explicitly install a Pillow version compatible with Streamlit (<11)
python -m pip install --quiet "pillow<11" customtkinter

:: Using python -m pip ensures we use the correct pip for the active env
:: python -m pip install --quiet --upgrade pillow customtkinter


echo.
echo Starting the program...
echo Logging to LOG.docx - this file does NOT contain any sensitive information - It's a text file but with a word document file extension to resolve problems uploading later.

python "%~dp0main.py" > "%~dp0LOG.docx" 2>&1

cls
echo.
echo ============================================================
echo Program finished. LOG.txt will be in the same folder.
echo This Window may close.
echo ============================================================
powershell sleep 5
