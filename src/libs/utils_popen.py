#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import subprocess

import libs.constants as C
from libs.config import GlobalConfig
from libs.objs import O_ExecuteCmd_Error 

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
            if self._gc.debug >= C.LOG_DEBUG_DEBUG:
                raise err
            
        if p.returncode or timeout_err:
            if timeout_err:
                OErr = O_ExecuteCmd_Error(p.returncode, out, err, "Timeout on execute:")
            else:
                OErr = O_ExecuteCmd_Error(p.returncode, out, err,  msg="")
            return (C.CHECK_ERROR, OErr)
        else:
            return (C.CHECK_OK, out if ret_data else "")
