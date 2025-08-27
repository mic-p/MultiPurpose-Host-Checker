# -*- coding: UTF-8 -*-

import os

from libs.config import GlobalConfig
from .base_check import BaseCheck
from libs.objs import O_check_work
import libs.constants as C

class Check_FsExists(BaseCheck):
    """"""
    __data_mandatory = (
                            ("event_on_exists", (bool, 0)),
                        )
    __data_optional = (
                            #("check_icmp_count", (int, 4)), 
                            #("", (fs_path, "")), 
                        )
    def __init__(self):
        """"""
        super(Check_FsExists).__init__()

        # class that represent our work
        self.check_work = O_check_work()
        
        self._host = None
        self._gc = GlobalConfig()
        
    def do_check(self, host, address):
        """"""
        self._address = address
        self._host = host
        self.check_work.host = host
        self.debug_log("Start FS Exists check for: %s"% (host.name, ))
        
        exists = os.path.exists(address)
        if self._host.specific_config.event_on_exists and exists:
            return (C.CHECK_MSG, "FS exists: %s" % self._host.specific_config.event_on_exists)
        elif not self._host.specific_config.event_on_exists and not exists:
            return (C.CHECK_MSG, "FS not exists: %s" % self._host.specific_config.event_on_exists)
        else:
            return (C.CHECK_OK, "")

    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_FsExists
