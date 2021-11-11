from pathlib import Path
from datetime import datetime


def ensure_dir(file_path):
    Path(file_path).mkdir(parents=True, exist_ok=True)


def ensure_file(file_path):
    Path(file_path).touch(exist_ok=True)


def format_date_float(time):
    return datetime.strptime(time, "%d %b %Y").timestamp()


def format_float_date(float):
    return datetime.fromtimestamp(float).strftime("%e %b %Y")
