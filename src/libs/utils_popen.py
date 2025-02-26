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
        
    def do_execute(self, cmd_exe,  vtimeout=None):
        """Execute a command"""
        timeout_err = 0
        try:
            p = subprocess.Popen(cmd_exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = p.communicate(timeout=vtimeout)
        except subprocess.TimeoutExpired:
            timeout_err = 1
        except Exception as err:
            err = (f"Unexpected {err=}, {type(err)=}")
            
        self._gc.log.debug("Command '%s', exit code: %s"% (cmd_exe, p.returncode, ))
        if p.returncode or timeout_err:
            if timeout_err:
                msg = "Timeout on execute: %s" % err
            else:
                msg = "Error on execute: %s" % err
            return (C.CHECK_ERROR, msg)
        else:
            return (C.CHECK_OK, "")
