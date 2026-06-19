@echo off
chcp 65001 >nul
echo TactiReader Portable Build
echo ==========================
echo.

:: Check PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [1/3] Installing PyInstaller...
    pip install pyinstaller
) else (
    echo [1/3] PyInstaller already installed
)

:: Check dependencies
echo [2/3] Checking dependencies...
pip install PyMuPDF PyQt5 markdown Pillow

:: Build
echo [3/3] Building...
python -m PyInstaller --noconfirm --clean --windowed --name TactiReader --icon=tactireader.ico --add-data "tactireader.png;." --add-data "docs/help.md;docs" --add-data "docs/about.md;docs" --add-data "docs/help_zh.md;docs" --add-data "docs/about_zh.md;docs" --add-data "tacti_reader;tacti_reader" tactireader.py

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

:: Create data folder
set DIST_DIR=dist\TactiReader
if not exist "%DIST_DIR%\data" mkdir "%DIST_DIR%\data"

echo.
echo Build complete!
echo Output: %DIST_DIR%\
echo.
echo Portable structure:
echo   TactiReader\
echo     +-- TactiReader.exe
echo     +-- data\        (settings stored here)
echo     +-- docs\
echo.
echo Copy the whole folder to another PC and it just works.
pause
