# Rutube Transcriber

Skachivает audio s Rutuba, transkribiruet cherez Whisper, soxranjaet v SQLite bazu.

## Ustanovka

```cmd
git clone https://github.com/YOUR_USERNAME/rutube-transcriber.git
cd rutube-transcriber
```

Zapusti `run.bat` i vyberi punkt 3 (Ustanovit pakety).

## Ispolzovanie

Zapusti `run.bat`:

```
1. Transkribacija     — skachat video i transkribirovat
2. Posmotret bazu     — spisok vseh video i transkribacij
3. Ustanovit pakety   — proverit i doustanovit vsyo neobhodimoe
4. Udalit pakety      — polnoe udalenie
```

## Struktura proekta

```
rutube-transcriber/
├── run.bat           — glavnyj fajl, zapuskat ego
├── main.py
├── downloader.py
├── transcriber.py
├── database.py
├── pyproject.toml
└── uv.lock
```
