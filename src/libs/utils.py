# -*- coding: UTF-8 -*-

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def conf_file_to_dict(f_path):
    # load the file
    d = {}
    with open(f_path) as check_env:
        for line in check_env.readlines():
            if line and "=" in line and not line.strip().startswith("#"):
                k, v = map(lambda x: x.strip(), line.split("="))
                d[k] = v
    return d

