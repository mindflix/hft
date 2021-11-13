from pathlib import Path
from datetime import datetime


def ensure_dir(file_path):
    Path(file_path).mkdir(parents=True, exist_ok=True)


def ensure_file(file_path):
    Path(file_path).touch(exist_ok=True)


def get_timestamp_ms(*args):
    tps_ms = []
    for arg in args:
        if (type(arg) == int or type(arg) == float):
            tp = arg
        elif (arg == None):
            tp = datetime.now().timestamp()
        else:
            date = str(arg).split()
            if (len(date) == 1):
                tp = datetime.strptime(arg, '%Y-%m-%d').timestamp()
            elif (len(date) == 2 and "." not in date[1]):
                tp = datetime.strptime(arg, '%Y-%m-%d %H:%M:%S').timestamp()
            else:
                tp = datetime.strptime(arg, '%Y-%m-%d %H:%M:%S.%f').timestamp()
        tp *= 1000
        tps_ms.append(tp)

    if (len(args) == 1):
        return tps_ms.pop()
    else:
        return tuple(tps_ms)


def get_fromtimestamp_ms(float):
    if (float == None):
        return datetime.now()
    else:
        return datetime.fromtimestamp(float/1000)
