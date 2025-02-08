# -*- coding: UTF-8 -*-

from .utils import  Singleton
from .objs import O_conf_log, O_conf_mphc
    
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
        
        self.log = None
        self.startup_done = False

    def __repr__(self):
        return "<GlobalConfig>%s; %s; %s" % (self.conf_log, self.conf_event_handler_smtp, self.conf_event_handler_gmail)

