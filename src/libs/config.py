# -*- coding: UTF-8 -*-

from .utils import  Singleton
from .objs import O_conf_log, O_conf_mphc, O_Hosts, O_checks_done, O_event_handlers, O_LocalConfig

class GlobalConfig(metaclass=Singleton):
    """Global container. Here we have:
        - configurations objects
        - useful functions used overall
    """
    def __init__(self):
        """"""
        self.conf_log = O_conf_log()
        self.conf_event_handler = dict()
        self.conf_mphc = O_conf_mphc()
        
        # commands to execute on some events error. see @doc for more info
        self.execute_cmd_event_error = ""
        self.execute_cmd_global_error = ""
        
        # event handlers list
        self.event_handles = O_event_handlers()

        #host configs
        self.hosts_config = O_Hosts()      
        
        # list of checks done after DoChecks.do_check class
        self.checks_done = O_checks_done()
        
        self.debug = False
        
        # path where save data and obj that cache into FS the informations
        self.path_data = ""
        self.local_config = O_LocalConfig()

        self.log = None
        self.startup_done = False

    def __repr__(self):
        return "<GlobalConfig>%s; %s; %s" % (self.conf_log, self.conf_event_handler, self.conf_mphc)

