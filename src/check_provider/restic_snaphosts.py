# -*- coding: UTF-8 -*-

import json
import time
import os

from libs.config import GlobalConfig
from libs import timeparse
from libs.objs import O_check_work
from libs.utils_popen import ExecuteCmd
from .base_check import BaseCheck

import libs.constants as C
import libs.utils as utils

class Check_Restic_snaphosts(BaseCheck):
    """"""
    __data_mandatory = (
                            #("", (str, "")),
                        )
    __data_optional = (
                            ("min_snapshots", (int, 1)),
                            ("snapshots_period", (str, "2d")),
                            ("restic_repo", (str, "")),
                            ("restic_exe", (str, "restic")),
                            ("restic_pwd", (str, "")),
                            ("access_key", (str, "")),
                            ("secret_key", (str, "")),
                            ("restic_envs_file", (str, "")),
                            #("", (str, "")),
                        )
    def __init__(self):
        """"""
        super(Check_Restic_snaphosts).__init__()

        # class that represent our work
        self.check_work = O_check_work()
        
        self._host = None
        self._gc = GlobalConfig()
        
    def do_check(self, host, address):
        """"""
        self._address = address
        self._host = host
        self.check_work.host = host
        self._gc.log.debug("Start Restic snapshots check for: %s"% (host.name, ))
        
        # create the command path
        cmd_exe = [host.specific_config.restic_exe, "-r", 
                    host.specific_config.restic_repo if host.specific_config.restic_repo else host.name, 
                    "snapshots", "--latest", str(host.specific_config.min_snapshots), "--json"]
        
        self._gc.log.debug("Execute Restic command: %s"% (cmd_exe, ))
        
        # create the env
        # if there is a specific env load, use it
        if host.specific_config.env:
            env = host.specific_config.env
        else:
            # unless use the one found on config
            env = {}
            data_env_toset =  (
                                ("access_key", "AWS_ACCESS_KEY_ID"), 
                                ("secret_key", "AWS_SECRET_ACCESS_KEY"), 
                                ("restic_pwd", "RESTIC_PASSWORD"), 
                        )
            for k_conf, k_env in data_env_toset:
                dta = getattr(host.specific_config, k_conf) 
                if dta:
                    env[k_env] = dta
        
        # and call the restic cmd
        errcode, msg = ExecuteCmd().do_execute(cmd_exe, ret_data=True, env_to_set=env)
        
        # if we have errors, return
        if errcode:
            return (errcode, msg)
        
        # load the json data
        data_read = json.loads(msg)
        # extract the time date
        snap_time = [time.strptime(line["time"][:18], "%Y-%m-%dT%H:%M:%S") for line in data_read]
        # calculate the valid period starting from now
        time_min = time.time() - timeparse.timeparse(host.specific_config.snapshots_period)
        time_min = time.gmtime(time_min)
        
        # extract only the valid snapshots
        snap_after = [snap for snap in filter(lambda x: x > time_min, snap_time)]
        
        # if not enough, return a message
        if len(snap_after) >= host.specific_config.min_snapshots:
            return (C.CHECK_OK, "")
        else:
            return (C.CHECK_MSG, "Not enough snapshots for %s: %s, we need: %s in period: %s" % (
                                    host.name, len(snap_after),
                                    host.specific_config.min_snapshots,
                                    host.specific_config.snapshots_period)
                            )
        
        #print (snap_time, time_min)
        return (errcode, msg)
        
    def startup_config_checks(self, config_obj):
        """Do startup configuration verification before start the work"""
        
        if not (config_obj.specific_config.restic_envs_file or config_obj.specific_config.restic_pwd):
            raise ValueError("No such file 'restic_envs_file' or 'restic_pwd' directive on: %s" % config_obj.name)
        
    def startup_load(self, config_obj):
        """Load internal data"""
        
        # create env for future use
        config_obj.specific_config.env = {}
        
        # continue only if the file exists
        if not (config_obj.specific_config.restic_envs_file and os.path.exists(config_obj.specific_config.restic_envs_file)):
            return
        
        # load the conf file and save it
        config_obj.specific_config.env = utils.conf_file_to_dict(config_obj.specific_config.restic_envs_file)

        
    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_Restic_snaphosts
