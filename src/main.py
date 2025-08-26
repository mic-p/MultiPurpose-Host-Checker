#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

from libs.config import GlobalConfig
from libs import startup, do_checks, do_events_handler, do_end_work

import libs.constants as C

class Work():
    def __init__(self):
        
        # startup application
        st = startup.Startup()
        # and do all the first works and configuration load
        st.DoStartupWork()
        
        self._gc = GlobalConfig()
        self._gc.log("Startup done! Start to check hosts")
        
        # start the checks
        checks = do_checks.DoChecks()
        checks.DoChecksWork()
        
        self._gc.log("Checks done! Start event handler")
        
        events = do_events_handler.DoEventsHandler()
        events.DoEventWork()
        
        self._gc.log("Events done! Start check for errors")
        
        end_work = do_end_work.DoEndWork()
        ret_code = end_work.DoEndWork()
        self._do_check_exit(ret_code)
        
    def _do_check_exit(self, ret_code):
        """End the checks and exit"""
        if ret_code == C.CHECK_DISASTER:
            msg_exit = "Some disaster errors presents. Maybe bug. See logs or enable execute_cmd_global_error. Exit 1"
            err_exit = 1
            f = self._gc.log.error
        else:
            msg_exit = "That's all, goodbye. See you next time!"
            f = self._gc.log
            err_exit = 0
        
        f(msg_exit)
        if err_exit:
            print(msg_exit)
        sys.exit(err_exit)
        


if __name__ == '__main__':
    Work()
