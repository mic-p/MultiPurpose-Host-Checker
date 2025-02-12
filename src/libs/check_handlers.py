# -*- coding: UTF-8 -*-

from check_provider import fs_exists, fs_changes, http_diff, http_ok, icmp,  dns_change


# to move to a better place and dynamic checks load
LST_CHECKS = {"fs_exists": fs_exists ,
                        "fs_changes": fs_changes, 
                        "http_diff": http_diff,
                        "http_ok": http_ok,
                        "icmp": icmp, 
                        "dns_change": dns_change}

class EventHandlers(object):
    """"""
    def __init___(self):
        pass
    
    def get_check_class(self, check_name):
        """"""
        return LST_CHECKS[check_name]
    
    def get_check_available(self):
        """"""
        return [x for x in LST_CHECKS]
