# -*- coding: UTF-8 -*-

import time
import traceback
import threading
import uuid
import functools 

from libs.config import GlobalConfig
from libs.objs import O_UnhandledError, O_CheckReport
from libs import timeparse

import libs.check_handlers as check_handlers
import libs.constants as C

class DoChecks(object):
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
    
    def DoChecksWork(self):
        """"""
        # create the hosts lists where work
        data_hosts = [host for host in sorted(self._gc.hosts_config,  key=lambda h: (self._gc.hosts_config[h].specific_config.priority, h))]
        
        # if we need to check simultaneously, do it with threads
        if self._gc.conf_mphc.n_checks_simultaneously > 1:
            #use threads
            self._gc.log.debug("Start checking with n %s threads" % self._gc.conf_mphc.n_checks_simultaneously)
            while (data_hosts or threading.active_count()-1):
                # iterate over the hosts. the order is from: priority + h_name
                if data_hosts and threading.active_count() -1 < self._gc.conf_mphc.n_checks_simultaneously:
                    host = data_hosts.pop()
                    t = threading.Thread(target=self._do_work, args=(host, ))
                    t.start()
                time.sleep(0.1)
        else:
            # no threads usage
            for host in data_hosts:
                self._do_work(host)
    
    def _log_work(self, work_uuid, text, funct_use=None):
        """"""
        msg = "%s-%s" % (work_uuid, text)
        
        if funct_use: funct_use = funct_use
        else: funct_use = self._gc.log.debug
        
        funct_use(msg)
        
    def _do_work(self, host):
        """Do the work for the host passed"""
        # configuration object
        
        obj_host = self._gc.hosts_config[host]
        check_name = obj_host.check
        work_uuid = uuid.uuid1().hex[:8]
        _log = functools.partial(self._log_work, work_uuid)
        
        if self._gc.host_check_startup:
            # check only the host(s) requested at startup
            if not host in self._gc.host_check_startup:
                _log("Host skipped: %s. We want here only: %s" % (host, self._gc.host_check_startup))
                return
        
        # check if the host is enable, otherwise skip it
        if not obj_host.specific_config.host_enable:
            _log("Host %s disable. Skipped", (host, ))
            return
        
        # check if we are called too early respect the configuration
        last_run_host = self._gc.local_config.data_last_run[obj_host.name]
        
        # if there is a mininum time to respect between two checks, calculate it
        if obj_host.specific_config.check_no_less_than:
            time_min = last_run_host + timeparse.timeparse(obj_host.specific_config.check_no_less_than)
            
            # verify if we need to pospone the check
            if not time.time() > time_min:
                _log("Called host: %s too early. Skip run" %  (host, ))
                return
        
        self._gc.local_config.data_last_run[obj_host.name] = time.time()
        
        # get the specific class
        cls = check_handlers.get_check_class(check_name).get_check_workers()
        check_class = cls()
        
        self._gc.checks_done.add_check(check_class)
        
        hosts_list = obj_host.host_details or (obj_host.name, )
        for address in hosts_list:
            # and call it!
            
            # verify the local data where we'll save the local data
            if not self._gc.local_config.check_data[obj_host.name]:
                # first usage, startup the variables
                self._gc.local_config.check_data[obj_host.name] = {}
            self._gc.local_config.check_data[obj_host.name].setdefault(address, None)
            
            ret_code = C.CHECK_ERROR
            # try to catch all the exception unhandled
            try:
                #call the event and check for the results
                if self._gc.debug == C.LOG_DEBUG_DDEBUG:
                    _log("specific_config: %s" % obj_host.specific_config)
                check_class.set_uuid(work_uuid )
                ret_code, msg_ret = check_class.do_check(obj_host, address)
                
                # we had a problem somewhere with the check that raise an error, save it for future report 
                if ret_code == C.CHECK_ERROR:
                    check_class.check_work.report_msg = O_UnhandledError("DoChecks - Check: %s - Host: %s" % (check_name, address), msg_ret)
                    check_class.check_work.report = C.CHECK_ERROR
                    _log(check_class.check_work.report_msg, self._gc.log.error)
                elif ret_code == C.CHECK_MSG:
                    check_class.check_work.report_msg = O_CheckReport(msg_ret)
                    check_class.check_work.report = C.CHECK_MSG
            except Exception as exc_obj:
                # if there is an error doing the check, trace it has disaster and try to trace the exception
                tb = traceback.format_exception(exc_obj)
                err = O_UnhandledError("DoChecks::%s::%s" % (check_name, address), tb)
                check_class.check_work.report = C.CHECK_DISASTER
                check_class.check_work.report_msg = err
                _log(err, self._gc.log.error)
                ret_code = C.CHECK_ERROR
                
                if self._gc.debug >= C.LOG_DEBUG_DEBUG:
                    raise
                                    
            if ret_code and not self._gc.conf_mphc.continue_on_check_problem:
                _log("Error happens on %s and continue_on_check_problem set True. Stop checks!" % check_name)
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
                        

