# -*- coding: UTF-8 -*-

from libs.config import GlobalConfig

class DoEndWork(object):
    """Do all the checks and work now that the MPHC has finished the check and event handler"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        
    def DoEndWork(self):
        """"""
        if not self._gc.global_errors:
            return 0
            
        for error in self._gc.global_errors:
            msg = "Disaster happens on: %s\n" % error.code_position
            msg += "".join(error.msg)
            self._gc.log.error(msg)
            
        return 1
