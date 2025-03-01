# -*- coding: UTF-8 -*-

import traceback

from libs.config import GlobalConfig
from libs.objs import O_UnhandledError, O_CheckReport

import libs.check_handlers as check_handlers
import libs.constants as C

class DoChecks(object):
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
    
    def DoChecksWork(self):
        """"""
        
        # iterate over the hosts. the order is from: priority + h_name
        for host in sorted(self._gc.hosts_config,  key=lambda h: (self._gc.hosts_config[h].specific_config.priority, h)):
            # configuration object
            obj_host = self._gc.hosts_config[host]
            check_name = obj_host.check
            
            # get the specific class
            cls = check_handlers.get_check_class(check_name).get_check_workers()
            check_class = cls()
            
            self._gc.checks_done.add_check(check_class)
            
            hosts_list = obj_host.host_details or (obj_host.name, )
            for address in hosts_list:
                # and call it!
                
                # verify the local data
                if not self._gc.local_config.check_data[obj_host.name]:
                    # first usage, startup the variables
                    self._gc.local_config.check_data[obj_host.name] = {}
                    self._gc.local_config.check_data[obj_host.name][address] = None
                
                ret_code = C.CHECK_ERROR
                # try to catch all the exception unhandled
                try:
                    #call the event and check for the results
                    ret_code, msg_ret = check_class.do_check(obj_host, address)
                    
                    # we had a problem somewhere with the check that raise an error, save it for future report 
                    if ret_code == C.CHECK_ERROR:
                        check_class.check_work.report_msg = O_UnhandledError("DoChecks::%s::%s" % (check_name, address), msg_ret)
                        check_class.check_work.report = C.CHECK_ERROR
                        self._gc.log.error(msg_ret)
                    elif ret_code == C.CHECK_MSG:
                        check_class.check_work.report_msg = O_CheckReport(msg_ret)
                        check_class.check_work.report = C.CHECK_ERROR
                except Exception as exc_obj:
                    # if there is an error doing the check, trace it has disaster and try to trace the exception
                    tb = traceback.format_exception(exc_obj)
                    err = O_UnhandledError("DoChecks::%s::%s" % (check_name, address), tb)
                    check_class.check_work.report = C.CHECK_DISASTER
                    check_class.check_work.report_msg = err
                    self._gc.log.error(err)
                    ret_code = C.CHECK_ERROR
                    
                    if self._gc.debug == 2:
                        raise
                                        
                if ret_code and not self._gc.conf_mphc.continue_on_check_problem:
                    self._gc.log.debug("Error happens on %s, stop checks!" % check_name)
                    break
                
                # verify if the check need to handle changes
                if not check_class.handle_changes() or ret_code != C.CHECK_OK:
                    continue
                
                if not self._gc.local_config.check_data[obj_host.name][address]:
                    # no such configuration for self._host
                    self._gc.local_config.check_data[obj_host.name][address] = msg_ret
                else:
                    # check if the data has changed
                    old_data = self._gc.local_config.check_data[obj_host.name][address]
                    self._gc.local_config.check_data[obj_host.name][address] = msg_ret
                    
                    #and if yes
                    if old_data != msg_ret:
                        chk_rep = O_CheckReport(check_class.format_changes(old_data, msg_ret))
                        check_class.check_work.report = C.CHECK_MSG
                        check_class.check_work.report_msg = chk_rep
                        #self._gc.global_messages.append(chk_rep)
                        

