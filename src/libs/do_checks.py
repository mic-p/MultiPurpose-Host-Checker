# -*- coding: UTF-8 -*-

from libs.config import GlobalConfig


class DoChecks(object):
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        
        # iterate over the hosts. the order is from: priority + h_name
        for host in sorted(self._gc.hosts_config,  key=lambda h: (self._gc.hosts_config[h].specific_config.priority, h)):
            obj_host = self._gc.hosts_config[host]
            check_name = obj_host.check
            cls = self._gc.checks_handler.get_check_class(check_name).get_check_workers()
            check_class = cls()
            check_class.do_check(obj_host)
            
            
    
    def DoChecksWork(self):
        """"""
        
