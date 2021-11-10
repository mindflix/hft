from pathlib import Path


def ensure_dir(file_path):
    Path(file_path).mkdir(parents=True, exist_ok=True)
