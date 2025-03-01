# -*- coding: UTF-8 -*-

import socket
import difflib

from libs.config import GlobalConfig
from .base_check import BaseCheck
from libs.objs import O_check_work
import libs.constants as C

import http.client as http_client
from urllib.parse import urlparse

class Check_HttpDiff(BaseCheck):
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
        super(Check_HttpDiff).__init__()

        # class that represent our work
        self.check_work = O_check_work()
        
        self._host = None
        self._gc = GlobalConfig()
        
    def do_check(self, host, address):
        """"""
        self._address = address
        self._host = host
        self.check_work.host = host
        self._gc.log.debug("Start Httpdiff check for: %s"% (host.name, ))
    
        ret_code = C.CHECK_ERROR
        q_ret = ""
        
        try:
            # verify if we need to connect with the S version of http
            if host.specific_config.use_https:
                f = http_client.HTTPSConnection
                prefix = "https://"
            else:
                f = http_client.HTTPConnection
                prefix = "http://"

            # connect
            if not address.startswith("http"):
                address = prefix + address
            
            # clean address
            addr = urlparse(address)
            
            conn = f(addr.netloc)
            try:
                conn.request("GET", addr.path or "/")
            except socket.gaierror:
                return (C.CHECK_ERROR, "Httpdiff Error!: No such name or service: %s" % str(addr))
            
            reply = conn.getresponse()
            
            # verify response.
            # TO-DO: implement config array into the configuratio
            if reply.status == 200:
                ret_code = C.CHECK_OK
                q_ret = reply.read()
            else:
                # response are different from our need, inspect the status and the reason
                ret_code = C.CHECK_MSG
                q_ret = "%s: %s(%s)\nDetails:\n" % (address, reply.status, reply.reason)
                for item in reply.msg.items():
                    # retrieve all the server headers
                    k, v = item
                    q_ret+= "%s: %s\n" % (k, v)
            #self._gc.log.debug("Httdiff check. Returns: %s" % (q_ret, ))
                
        except Exception as err:
            raise err
                
        return (ret_code, q_ret)

    def handle_changes(self):
        """Indicate that we are able to handle changes"""
        return True
        
    def format_changes(self, old, new):
        """Format changes"""
        
        old = old.splitlines(keepends=True)
        new = new.splitlines(keepends=True)

        d = difflib.Differ()
        result = list(d.compare(old, new))
        dta = "\n".join(result)
        
        return "Http page %s change content:\n%s\n" % (self._address, dta)

    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_HttpDiff
