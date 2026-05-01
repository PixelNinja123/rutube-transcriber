import whisper
import warnings
import tqdm
import tqdm.std
from pathlib import Path

MODEL_NAME = "medium"

_model = None


def _get_model():
    global _model
    if _model is None:
        print("[transcriber] Zagruzhaem model Whisper...")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _model = whisper.load_model(MODEL_NAME)
        print("[transcriber] Model zagružena.")
    return _model


def transcribe(audio_path: str) -> str:
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(f"Fajl ne najden: {audio_path}")

    model = _get_model()
    print("[transcriber] Nachinaem transkribaciju...")

    original_tqdm = tqdm.std.tqdm

    class ProgressBar(tqdm.std.tqdm):
        def update(self, n=1):
            super().update(n)
            if self.total:
                percent = int(self.n / self.total * 100)
                bar = "#" * (percent // 5) + "-" * (20 - percent // 5)
                print(f"\r  [{bar}] {percent}%", end="", flush=True)

    tqdm.std.tqdm = ProgressBar
    tqdm.tqdm = ProgressBar

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = model.transcribe(str(path), language="ru", verbose=False)
    finally:
        tqdm.std.tqdm = original_tqdm
        tqdm.tqdm = original_tqdm

    print(f"\r[transcriber] Gotovo! Simvolov: {len(result['text'].strip())}")
    return result["text"].strip()
