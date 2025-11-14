# -*- coding: UTF-8 -*-

from libs.config import GlobalConfig
from .base_check import BaseCheck
from libs.objs import O_check_work, T_AInt
import libs.constants as C

from ._base_http import do_get_reply

class Check_HttpOk(BaseCheck):
    """"""
    __data_mandatory = (
                            #("", (str, "")),  
                        )
    __data_optional = (
                            ("use_https", (bool, 1)),
                            ("http_status_ok", (T_AInt, "200")), 
                        )
    def __init__(self):
        """"""
        super(Check_HttpOk).__init__()

        # class that represent our work
        self.check_work = O_check_work()
        
        self._host = None
        self._gc = GlobalConfig()
        
    def do_check(self, host, address):
        """"""
        self._address = address
        self._host = host
        self.check_work.host = host
        self.debug_log("Start HttpOk check for: %s"% (host.name, ))
    
        try:
            # connect to the host
            ret_code, reply = do_get_reply(host, address, "HttpOk Error!")
        except Exception as err:
            raise err
        
        # there is an error, return and signal it
        if ret_code != C.CHECK_OK:
            return (ret_code, reply)
        
        if reply.status in host.specific_config.http_status_ok:
            ret_code = C.CHECK_OK
            q_ret = "Ok! %s" % reply.status
        else:
            # response are different from our need, inspect the status and the reason
            ret_code = C.CHECK_MSG
            q_ret = "Error! %s: %s(%s)\nDetails:\n" % (address, reply.status, reply.reason)
            for item in reply.msg.items():
                # retrieve all the server headers
                k, v = item
                q_ret+= "%s: %s\n" % (k, v)
        self.debug_log("HttpOk check. Host: %s. Returns: %s" % (address, q_ret, ))
                
        return (ret_code, q_ret)
    
        
    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional

def get_check_workers():
    return Check_HttpOk
