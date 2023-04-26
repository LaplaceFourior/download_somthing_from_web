@echo off

pip show virtualenv > nul
if %errorlevel% neq 0 (
    echo Installing virtualenv...
    pip install virtualenv
) else (
    echo virtualenv already installed.
)

echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo Activating virtual environment...
call venv\Scripts\Activate.bat
echo Virtual environment activated.

:: Check if required packages are already installed
for /f "usebackq delims=" %%i in ("requirements/Win.txt") do set /p required_packages= < "%%i"
for /f "delims==" %%i in ('pip freeze') do set installed_packages=!installed_packages! %%i
set missing_packages=
for %%i in (%required_packages%) do (
    echo !installed_packages! | findstr /c:"%%i" > nul || set missing_packages=!missing_packages! %%i
)
if defined missing_packages (
    echo Installing required packages...
    pip install %missing_packages%
) else (
    echo Required packages already installed.
)

echo Packages installed.
echo Starting application...
start /B python main.py