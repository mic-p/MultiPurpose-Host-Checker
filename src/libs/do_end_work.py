# -*- coding: UTF-8 -*-

import libs.local_config as local_config
import libs.constants as C

from libs.config import GlobalConfig
from event_handler import execute_cmd


class DoEndWork(object):
    """We did all the checks and works.
        Now closeup the and let's do the ending work
        """
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        
    def DoEndWork(self):
        """Do the ending works before exit"""
        # save data
        self._save_local()
        
        # verify if there is some errors with the checks
        check_report = self._gc.checks_done.get_check_report_disaster()
        if not check_report:
            return C.CHECK_OK
        
        err_ret = C.CHECK_DISASTER
        # return if there is no need to call external command on global error
        if not self._gc.execute_cmd_global_error:
            return err_ret
        
        for host_work in check_report:
            # and call the execute_cmd_global_error for every error present
            c = execute_cmd.Evt_ExecuteCmd()
            c.do_event(host_work)
        
        return err_ret

    def _save_local(self):
        """"""
        lc = local_config.LocalConfig()
        lc.save(self._gc.local_config.check_data)
        
