@echo off
chcp 65001 >nul
echo ================================
echo  Удаление Rutube Transcriber
echo ================================
echo.

:: Удаляем Python-пакеты
echo [1/4] Удаляем Python-пакеты...
pip uninstall openai-whisper yt-dlp torch torchvision torchaudio -y
echo.

:: Удаляем модель Whisper
echo [2/4] Удаляем модель Whisper...
set WHISPER_CACHE=%USERPROFILE%\.cache\whisper
if exist "%WHISPER_CACHE%" (
    rmdir /s /q "%WHISPER_CACHE%"
    echo Удалено: %WHISPER_CACHE%
) else (
    echo Папка не найдена, пропускаем.
)
echo.

:: Удаляем ffmpeg
echo [3/4] Удаляем ffmpeg...
winget uninstall ffmpeg >nul 2>&1
if errorlevel 1 (
    choco uninstall ffmpeg -y >nul 2>&1
    if errorlevel 1 (
        echo ffmpeg не найден или установлен вручную — удали сам из PATH.
    ) else (
        echo ffmpeg удалён через chocolatey.
    )
) else (
    echo ffmpeg удалён через winget.
)
echo.

:: Удаляем папку проекта
echo [4/4] Удаляем папку проекта...
set PROJECT_DIR=%~dp0
echo Будет удалена папка: %PROJECT_DIR%
choice /c YN /m "Удалить?"
if errorlevel 2 (
    echo Пропускаем.
) else (
    cd %USERPROFILE%
    rmdir /s /q "%PROJECT_DIR%"
    echo Папка удалена.
)

echo.
echo ================================
echo  Готово! Всё удалено.
echo ================================
pause
