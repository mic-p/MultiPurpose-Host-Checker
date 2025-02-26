# -*- coding: UTF-8 -*-

from libs.config import GlobalConfig
from .base_check import BaseCheck
from libs.objs import O_check_work
import libs.constants as C

import http.client as http_client

class Check_HttpOk(BaseCheck):
    """"""
    __data_mandatory = (
                            #("", (str, "")),  
                        )
    __data_optional = (
                            ("use_https", (bool, 1)),
                            #("", (str, "")), 
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
        self._gc.log.debug("Start HttpOk check for: %s"% (host.name, ))
    
        ret_code = C.CHECK_ERROR
        q_ret = ""
        
        try:
            # verify if we need to connect with the S version of http
            if host.specific_config.use_https:
                f = http_client.HTTPSConnection
            else:
                f = http_client.HTTPConnection
            1/0
            # connect
            conn = f(self._address)
            conn.request("GET", "/")
            reply = conn.getresponse()
            
            # verify response.
            # TO-DO: implement config array into the configuratio
            if reply.status == 200:
                ret_code = C.CHECK_OK
            else:
                # response are different from our need, inspect the status and the reason
                ret_code = C.CHECK_MSG
                q_ret = "%s: %s(%s)\nDetails:\n" % (address, reply.status, reply.reason)
                for item in reply.msg.items():
                    # retrieve all the server headers
                    k, v = item
                    q_ret+= "%s: %s\n" % (k, v)
            self._gc.log.debug("HttpOk check. Return: %s" % (q_ret, ))
                
        except Exception as err:
            raise err
                
        return (ret_code, q_ret)
    
        
    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional

def get_check_workers():
    return Check_HttpOk
