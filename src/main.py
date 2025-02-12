#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from libs.config import GlobalConfig

from libs import startup, do_checks, do_events_handler


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
        
        self._gc.log.debug("Checks done! Start event hanndler")
        
        do_events_handler.DoEventsHandler()
        


if __name__ == '__main__':
    Work()
