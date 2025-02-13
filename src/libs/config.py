# -*- coding: UTF-8 -*-

from .utils import  Singleton
from .objs import O_conf_log, O_conf_mphc, O_checks, O_Hosts, O_checks_done, O_event_handlers

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
        
        # event handlers list
        self.event_handles = O_event_handlers()

        #host configs
        self.hosts_config = O_Hosts()      
        
        # list of checks done after DoChecks.do_check class
        self.checks_done = O_checks_done()
        
        self.debug = False
        self.path_data = ""

        self.log = None
        self.startup_done = False

    def __repr__(self):
        return "<GlobalConfig>%s; %s; %s" % (self.conf_log, self.conf_event_handler, self.conf_mphc)

