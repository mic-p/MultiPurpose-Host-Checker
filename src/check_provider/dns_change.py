# -*- coding: UTF-8 -*-

from libs.config import GlobalConfig
from .base_check import BaseCheck
from libs.objs import O_check_work, T_AStr

import libs.constants as C

import dns.resolver as D
# https://gist.github.com/akshaybabloo/2a1df455e7643926739e934e910cbf2e

class Check_DnsChange(BaseCheck):
    """"""
    __data_mandatory = (
                            ("record_type", (T_AStr, "")),  
                        )
    __data_optional = (
                            ("check_icmp_count", (int, 4)), 
                            #("", (str, "")), 
                        )
    def __init__(self):
        """"""
        super(Check_DnsChange).__init__()
        
        self._gc = GlobalConfig()

        # class that represent our work
        self.check_work = O_check_work()
        
        self._host = None
        self._gc = GlobalConfig()
        
    def do_check(self, host, address):
        """"""
        self._address = address
        self._host = host
        self.check_work.host = host
        
        self.debug_log("Start DNS Change check for: %s"% (address, ))

        ret_code = C.CHECK_ERROR
        q_ret = []
        try:
            for rt in host.specific_config.record_type:
                for x in D.resolve(self._address, rt):
                    ret = x.to_text()
                    q_ret.append((rt, ret))
            
            q_ret.sort()
            ret_code = C.CHECK_OK
        except Exception as err:
            raise err
            #msg = (f"Unexpected {err=}, {type(err)=}")
            #q_ret = msg
                
        return (ret_code, q_ret)
    
    def handle_changes(self):
        """Indicate that we are able to handle changes"""
        return True
        
    def format_changes(self, old, new):
        """Format changes"""
        
        return "Dns record: %s for address: %s changed from: %s to %s" % (self._host.specific_config.record_type, self._address, old, new)

    def _recursive_A_resolve(self, data):
        """future feature for try to check all the DNS tree"""
        
    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_DnsChange
