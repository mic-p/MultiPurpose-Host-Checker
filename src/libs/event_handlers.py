# -*- coding: UTF-8 -*-

from event_handler import email_gmail, email_smtp, execute_cmd

# to move to a better place and dynamic checks load
LST_EVENTS = {"gmail": email_gmail ,
                        "smtp": email_smtp, 
                        "cmd": execute_cmd,}

class EventHandlers(object):
    """"""
    def __init___(self):
        pass
    
    def load_event_handlers(self):
        """Startup the event handlers. Future use for load external evts"""
    
def get_event_class(event_name):
    """"""
    return LST_EVENTS[event_name]

def get_event_available():
    """"""
    return [x for x in LST_EVENTS]
