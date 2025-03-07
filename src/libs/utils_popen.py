#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import subprocess
from libs.config import GlobalConfig
import libs.constants as C

class ExecuteCmd(object):
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        
    def do_execute(self, cmd_exe,  vtimeout=None, shell=False, ret_data=False, env_to_set=None):
        """Execute a command"""
        timeout_err = 0
        try:
            p = subprocess.Popen(cmd_exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=shell, env=env_to_set)
            out, err = p.communicate(timeout=vtimeout)
        except subprocess.TimeoutExpired:
            timeout_err = 1
        except Exception as err:
            err = (f"Unexpected {err=}, {type(err)=}")
            if self._gc.debug == 2:
                raise
            
        if p.returncode or timeout_err:
            if timeout_err:
                msg = "Timeout on execute: %s" % err
            else:
                msg = "Exit code: %s. Message error: %s" % (p.returncode, err)
            return (C.CHECK_ERROR, msg)
        else:
            return (C.CHECK_OK, out if ret_data else "")
