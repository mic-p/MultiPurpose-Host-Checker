# -*- coding: UTF-8 -*-

import traceback

from libs.config import GlobalConfig
from libs.objs import O_GlobalError

class DoEventsHandler(object):
    """"""
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
    
    def DoEventWork(self):
        """"""
        # iterate over the hosts. the order is from: priority + h_name
        for host_work in sorted(self._gc.checks_done.get_errors()):
            # configuratio object
            #check_name = obj_host.check
            
            # look for the event name (on_event is the name of the event to call when errors occured. it is the option in the config file)
            event_name = host_work.check_work.host.on_event
            
            # retrieve the corresponding module for on_event
            evth_module = self._gc.event_handles[event_name]
            event_class = evth_module.get_event_workers()()
            
            try:
                event_class.do_event(host_work)
            except Exception as exc_obj:
                # if there is an error doing the check, trace it has disaster and try to trace the exception
                tb = traceback.format_exception(exc_obj)

                #tb_str = ''.join(traceback.format_exception(None, exc_obj, exc_obj.__traceback__))
                #msg = "Disaster on check: %s\n" % event_name
                #msg += tb_str
                #self._gc.log.error(msg)
                
                err = O_GlobalError("DoEventsHandler::%s" % event_name, tb)
                self._gc.global_errors.append(err)
        
            
