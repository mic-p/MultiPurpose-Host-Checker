# -*- coding: UTF-8 -*-

import traceback

from libs.config import GlobalConfig
from libs.report_msgs import check_build_msgs

#from libs.objs import O_UnhandledError

class DoEventsHandler(object):
    """"""
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
    
    def DoEventWork(self):
        """"""
        # iterate over the hosts
        for host_work in self._gc.checks_done.get_check_report():
            # configuration object
            #check_name = obj_host.check
            
            # look for the event name (on_event is the name of the event to call when errors occured. it is the option in the config file)
            event_name = host_work.check_work.host.on_event
            
            # retrieve the corresponding module for on_event
            evth_module = self._gc.event_handles[event_name]
            event_class = evth_module.get_event_workers()()
            
            try:
                if self._gc.debug == 2:
                    self._gc.log.debug("Skip calling :%s with: %s" % (event_name, event_class, ))
                    msg_text = check_build_msgs(host_work.check_work.report) % host_work.check_work.report_msg.msg
                    self._gc.log.debug("Message not sent: %s" % msg_text)
                else:
                    event_class.do_event(host_work)
                        
            except Exception as exc_obj:
                # if there is an error doing the check, trace it has disaster and try to trace the exception
                tb = traceback.format_exception(exc_obj)

                msg = "Disaster on Event: %s\n%s" % (event_name, tb)
                self._gc.log.error(msg)
                
                if self._gc.debug == 2:
                    raise
                
                #err = O_UnhandledError("DoEventsHandler::%s" % event_name, tb)
                #self._gc.global_messages.append(err)
        
            
