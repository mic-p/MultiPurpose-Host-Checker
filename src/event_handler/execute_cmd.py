#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from libs.utils_popen import ExecuteCmd
from libs.config import GlobalConfig

class Evt_ExecuteCmd(object):
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        
    def do_event(self, host_work):
        """"""
        event_name = host_work.check_work.host.on_event
        cmd_execute_config = self._gc.conf_event_handler[event_name]
        
        self._gc.log.debug("ExecuteCmd: %s, %s" % (event_name,  cmd_execute_config.execute_cmd))
        """
        # Execute commands. Possibile variables passed to cmd_to_execute
            # $c -> check|event name
            # $h -> host (valid only for events, null otherwise)
            # $r -> return code from check
            # $f -> random path to a file that contains the information that the check|event returns to explain the error. It's up to the program delete it
        """
        ExecuteCmd().do_execute

def get_event_workers():
    return Evt_ExecuteCmd
