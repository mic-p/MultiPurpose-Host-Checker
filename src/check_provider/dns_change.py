# -*- coding: UTF-8 -*-

from libs.config import GlobalConfig
from .base_check import BaseCheck

import dns.resolver as D
# https://gist.github.com/akshaybabloo/2a1df455e7643926739e934e910cbf2e

class Check_DnsChange(BaseCheck):
    """"""
    __data_mandatory = (
                            ("record_type", (str, "")),  
                        )
    __data_optional = (
                            ("check_icmp_count", (int, 4)), 
                            #("", (str, "")), 
                        )
    def __init__(self):
        """"""
        super(Check_DnsChange).__init__()
        
        self._gc = GlobalConfig()

    def do_check(self,  host):
        """"""
        self._host = host
        self._gc.log.debug("Start DNS Change check for: %s"% (host.name, ))

        D.query
        for x in D.resolve("microsoft.com", "TXT"): 
            x.to_text()

    
    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_DnsChange
