@echo off
chcp 65001 >nul
echo ================================
echo  Ustanovka Rutube Transcriber
echo ================================
echo.

:: Proverjaem Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [OSHIBKA] Python ne najden.
    echo Skachaj i ustanovi Python s https://python.org/downloads
    echo Pri ustanovke postav' galochku "Add Python to PATH"
    pause
    exit /b 1
)

echo [1/3] Python najden
echo.

:: Proverjaem ffmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [2/3] ffmpeg ne najden. Ustanavlivaem cherez winget...
    winget install ffmpeg
    if errorlevel 1 (
        echo.
        echo [OSHIBKA] Ne udalos' ustanovit' ffmpeg avtomaticheski.
        echo Ustanovi vruchnuju: winget install ffmpeg
        echo Ili cherez chocolatey: choco install ffmpeg
        pause
        exit /b 1
    )
) else (
    echo [2/3] ffmpeg najden
)

echo.
echo [3/3] Ustanavlivaem Python-zavisimosti...
pip install -r requirements.txt

echo.
echo ================================
echo  Gotovo! Zapuskaj: python main.py
echo ================================
pause
