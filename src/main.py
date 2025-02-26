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
        self._gc.log.debug("Startup done! Start to check hosts")
        
        # start the checks
        checks = do_checks.DoChecks()
        checks.DoChecksWork()
        
        self._gc.log.debug("Checks done! Start event handler")
        
        events = do_events_handler.DoEventsHandler()
        events.DoEventWork()
        
        self._gc.log.debug("Events done! Start check for errors")
        
        end_work = do_end_work.DoEndWork()
        ret_code = end_work.DoEndWork()
        
        if ret_code == C.CHECK_ERROR:
            msg_exit = "Some errors presents, exit 1"
            err_exit = 1
        else:
            msg_exit = "That's all, goodbye. See you next time!"
            err_exit = 0
        
        self._gc.log.debug(msg_exit)
        sys.exit(err_exit)
        
        
        


if __name__ == '__main__':
    Work()
