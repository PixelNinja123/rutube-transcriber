@echo off
echo ================================
echo  Установка Rutube Transcriber
echo ================================
echo.

:: Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден.
    echo Скачай и установи Python с https://python.org/downloads
    echo При установке поставь галочку "Add Python to PATH"
    pause
    exit /b 1
)

echo [1/3] Python найден
echo.

:: Проверяем ffmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [2/3] ffmpeg не найден. Устанавливаем через winget...
    winget install ffmpeg
    if errorlevel 1 (
        echo.
        echo [ОШИБКА] Не удалось установить ffmpeg автоматически.
        echo Установи вручную: winget install ffmpeg
        echo Или через chocolatey: choco install ffmpeg
        pause
        exit /b 1
    )
) else (
    echo [2/3] ffmpeg найден
)

echo.
echo [3/3] Устанавливаем Python-зависимости...
pip install -r requirements.txt

echo.
echo ================================
echo  Готово! Запускай: python main.py
echo ================================
pause
