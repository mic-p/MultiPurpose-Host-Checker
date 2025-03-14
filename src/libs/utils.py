# -*- coding: UTF-8 -*-

from libs import objs

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

def load_data_opt(config, section, opt_name, ftype, fallback=None):
    """Load the data following"""
    if issubclass(ftype, bool):
        fcall_str = "getboolean"
    elif issubclass(ftype, int):
        fcall_str = "getint"
    elif issubclass(ftype, str):
        fcall_str = "get"
    elif issubclass(ftype, (objs.T_AStr, objs.T_AInt)):
        v_read = [x.strip() for x in config.get(section, opt_name, fallback=fallback).split(",")]
        if issubclass(ftype, objs.T_AStr):
            fcall = str
        elif issubclass(ftype, objs.T_AInt):
            fcall = int
            if not v_read:
                v_read = fallback
        else:
            raise ValueError("load_data_opt:: Bug!")
        return [x for x in map(lambda x: fcall(x), v_read)]
    else:
        raise ValueError("Type %s not supported" % str(ftype))
    # set to the configuration the data loaded.
    # here we use a workaround for a BUG of configparser that raise an exception when getint is called and the option is empty... argh!
    if fcall_str in ("getint", "getboolean") and config.get(section, opt_name, fallback="") == "":
            if not fallback:
                valuetoset = 0
            else:
                valuetoset = fallback
    else:
        fcall = getattr(config, fcall_str)
        valuetoset = fcall(section, opt_name, fallback=fallback)
    
    return valuetoset
