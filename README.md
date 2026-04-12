# Rutube Transcriber

Скачивает аудио с Рутуба, транскрибирует его через Whisper и сохраняет в локальную SQLite базу.

## Установка

### 1. Скачай репозиторий

```cmd
git clone https://github.com/ВАШ_НИКНЕЙМ/rutube-transcriber.git
cd rutube-transcriber
```

Или скачай ZIP через кнопку **Code → Download ZIP** на GitHub и распакуй.

### 2. Запусти установку

Дважды кликни на **setup.bat** — он сам проверит и установит всё необходимое:
- Python (если не установлен — покажет ссылку)
- ffmpeg
- Python-зависимости (yt-dlp, openai-whisper)

> ⚠️ При первом запуске `python main.py` Whisper скачает модель (~1.5 ГБ). Это только один раз.

## Использование

```cmd
# Спросит ссылку интерактивно
python main.py

# Передать ссылку сразу
python main.py https://rutube.ru/video/...

# Показать все видео в базе
python main.py --list

# Показать транскрипцию конкретного видео
python main.py --show <video_id>
```

## Структура проекта

```
rutube-transcriber/
├── main.py           # точка входа
├── downloader.py     # скачивание аудио с Рутуба
├── transcriber.py    # транскрибация через Whisper
├── database.py       # работа с SQLite
├── requirements.txt  # зависимости
├── setup.bat         # автоустановка для Windows
└── .gitignore
```

## Как это работает

1. `yt-dlp` скачивает аудиодорожку с Рутуба
2. `Whisper` транскрибирует аудио в текст (модель `medium`, язык `ru`)
3. Ссылка на видео и транскрипция сохраняются в `transcriptions.db`
4. Аудиофайл удаляется — в базе остаётся только текст

Одно и то же видео можно передать повторно — дубли игнорируются.
