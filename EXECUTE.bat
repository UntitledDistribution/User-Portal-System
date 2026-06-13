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

:: Initialize flag to track if Python is found
set "PYTHON_FOUND=0"

:: ============================================================
:: 2. FIND ANACONDA ENVIRONMENT OR FALLBACK TO SYSTEM PYTHON
:: ============================================================

:: Check for Anaconda in common locations
if exist "C:\ProgramData\Anaconda3\Scripts\activate.bat" (
    set "ANACONDA_PATH=C:\ProgramData\Anaconda3"
    echo Found Anaconda at: %ANACONDA_PATH%
    goto :ACTIVATE_CONDA
) else if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
    set "ANACONDA_PATH=%USERPROFILE%\anaconda3"
    echo Found Anaconda at: %ANACONDA_PATH%
    goto :ACTIVATE_CONDA
) else (
    echo Anaconda not found. Checking for system Python...
    goto :CHECK_SYSTEM_PYTHON
)

:ACTIVATE_CONDA
:: Activate the conda base environment
call "%ANACONDA_PATH%\Scripts\activate.bat" "%ANACONDA_PATH%"
set "PYTHON_FOUND=1"
goto :INSTALL_DEPS

:CHECK_SYSTEM_PYTHON
:: Check if 'python' is available in the system PATH
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Found system Python. Proceeding without Anaconda.
    set "PYTHON_FOUND=1"
    goto :INSTALL_DEPS
) else (
    goto :NO_PYTHON_ERROR
)

:NO_PYTHON_ERROR
cls
echo ============================================================
echo    CRITICAL ERROR: CANNOT START THE TEST ON THIS DEVICE.
echo ============================================================
echo ERROR: Neither Anaconda nor a standard Python installation was found.
echo.
echo Please install Python (https://www.python.org) or Anaconda.
echo Ensure 'Add Python to PATH' is checked during installation.
echo.
pause
exit /b 1

:INSTALL_DEPS
if "%PYTHON_FOUND%"=="1" (
    echo.
    echo Installing/Verifying dependencies (Pillow < 11, CustomTkinter)...
    :: Using python -m pip ensures we use the pip associated with the active python
    python -m pip install --quiet "pillow<11" customtkinter
    
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo WARNING: Package installation encountered issues. Attempting to run anyway...
    )
)

:: ============================================================
:: 3. RUN THE PROGRAM
:: ============================================================
echo.
echo Starting the program...
echo Logging to LOG.txt (Text file with .docx extension for upload compatibility).

:: Run the main script and redirect output to LOG.txt
python "%~dp0main.py" > "%~dp0LOG.txt" 2>&1

if %ERRORLEVEL% EQU 0 (
    cls
    echo.
    echo ============================================================
    echo Program finished successfully.
    echo LOG.txt is in the same folder.
    echo This Window will close in 5 seconds.
    echo ============================================================
) else (
    cls
    echo.
    echo ============================================================
    echo Program finished with ERRORS.
    echo Please check LOG.txt for details.
    echo This Window will close in 10 seconds.
    echo ============================================================
    timeout /t 10
    exit /b %ERRORLEVEL%
)

timeout /t 5
