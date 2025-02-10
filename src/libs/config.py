# -*- coding: UTF-8 -*-

from .utils import  Singleton
from .objs import O_conf_log, O_conf_mphc, O_conf_host_default, O_checks
    
class GlobalConfig(metaclass=Singleton):
    """Global container. Here we have:
        - configurations objects
        - useful functions osed overall
    """
    def __init__(self):
        """"""
        self.conf_log = O_conf_log()
        self.conf_event_handler = dict()
        self.conf_mphc = O_conf_mphc()
        
        # checks list
        self.checks = O_checks()
        
        #host configs
        self.host_default = O_conf_host_default()
        self.hosts_config = {}        

        self.debug = False
        self.path_data = ""

        self.log = None
        self.startup_done = False

    def __repr__(self):
        return "<GlobalConfig>%s; %s; %s" % (self.conf_log, self.conf_event_handler, self.conf_mphc)

