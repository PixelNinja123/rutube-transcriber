@echo off
cd /d "%~dp0"

:menu
cls
echo ================================
echo  Rutube Transcriber
echo ================================
echo.
echo  1. Transkribacija
echo  2. Posmotret bazu
echo  3. Udalit pakety
echo.
set /p choice="Vyberi: "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto list
if "%choice%"=="3" goto uninstall
goto menu

:setup
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Python ne najden.
    echo Skachaj s https://python.org/downloads
    echo Pri ustanovke postavj galochku "Add Python to PATH"
    pause
    goto menu
)

uv --version >nul 2>&1
if errorlevel 1 (
    echo Ustanavlivaem uv...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    call "%~f0"
    exit /b
)

ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo Ustanavlivaem ffmpeg...
    winget install ffmpeg
    for /f "tokens=*" %%i in ('powershell -Command "[System.Environment]::GetEnvironmentVariable(\"PATH\", \"Machine\")"') do set "PATH=%%i;%PATH%"
    ffmpeg -version >nul 2>&1
    if errorlevel 1 (
        echo ffmpeg ustanovlen. Zakroj okno i zapusti run.bat zanovo.
        pause
        exit /b 0
    )
)

uv sync >nul 2>&1

uv run main.py
echo.
pause
goto menu

:list
echo.
uv run main.py --list
echo.
pause
goto menu

:uninstall
echo.
echo Udaljaem model Whisper...
set WHISPER_CACHE=%USERPROFILE%\.cache\whisper
if exist "%WHISPER_CACHE%" (
    rmdir /s /q "%WHISPER_CACHE%"
    echo OK: %WHISPER_CACHE%
) else (
    echo Ne najdeno, propuskaem.
)

echo Udaljaem ffmpeg...
winget uninstall ffmpeg >nul 2>&1
if errorlevel 1 (
    choco uninstall ffmpeg -y >nul 2>&1
    if errorlevel 1 (
        echo ffmpeg ne najden, propuskaem.
    ) else (
        echo OK: udalon cherez chocolatey.
    )
) else (
    echo OK: udalon cherez winget.
)

echo.
choice /c YN /m "Udalit papku proekta?"
if errorlevel 2 goto menu
cd %USERPROFILE%
rmdir /s /q "%~dp0"
exit /b 0
