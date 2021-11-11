from pathlib import Path
from datetime import datetime


def ensure_dir(file_path):
    Path(file_path).mkdir(parents=True, exist_ok=True)


def ensure_file(file_path):
    Path(file_path).touch(exist_ok=True)


def format_utc_float(utc):
    utc_list = str(utc).split()
    if (len(utc_list) == 1):
        return datetime.strptime(utc, '%Y-%m-%d').timestamp()
    if (len(utc_list) == 2):
        if ("." in utc_list[1]):
            return datetime.strptime(utc, '%Y-%m-%d %H:%M:%S.%f').timestamp()
        else:
            return datetime.strptime(utc, '%Y-%m-%d %H:%M:%S').timestamp()


def format_float_utc(float):
    return str(datetime.utcfromtimestamp(float))
