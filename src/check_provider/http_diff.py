# -*- coding: UTF-8 -*-

from libs.config import GlobalConfig
from .base_check import BaseCheck


class Check_HttpDiff(BaseCheck):
    """"""
    __data_mandatory = (
                            #("", (str, "")),  
                        )
    __data_optional = (
                            #("check_icmp_count", (int, 4)),
                            #("", (str, "")), 
                        )
    def __init__(self):
        """"""
        super(Check_HttpDiff).__init__()

        self._gc = GlobalConfig()

    def do_check(self,  host):
        """"""
        self._host = host
        self._gc.log.debug("Start Httpdiff check for: %s"% (host.name, ))

    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_HttpDiff
