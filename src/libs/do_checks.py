# -*- coding: UTF-8 -*-

import traceback

from libs.config import GlobalConfig
import libs.check_handlers as check_handlers

from libs.objs import O_GlobalError

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
                try:
                    check_class.do_check(obj_host, address)
                    if check_class.check_work.error and not self._gc.conf_mphc.continue_on_check_problem:
                        self._gc.log.debug("Error happens on %s, stop checks" % check_name)
                        break

                except Exception as exc_obj:
                    # if there is an error doing the check, trace it has disaster and try to trace the exception
                    check_class.check_work.error = 100
                    tb = traceback.format_exception(exc_obj)
                    #tb_str = '\n'.join(traceback.format_exception(None, exc_obj, exc_obj.__traceback__))
                    #msg = "Disaster on check: %s\n" % check_name
                    #msg += tb_str
                    #self._gc.log.error(msg)
                    
                    err = O_GlobalError("DoChecks::%s::%s" % (check_name, address), tb)
                    self._gc.global_errors.append(err)
                    
                    if not self._gc.conf_mphc.continue_on_check_problem:
                        self._gc.log.debug("Error happens on %s, stop checks" % check_name)
                        break

