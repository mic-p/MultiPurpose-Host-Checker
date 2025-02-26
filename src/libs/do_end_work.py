# -*- coding: UTF-8 -*-

import libs.local_config as local_config
import libs.objs as O
import libs.constants as C

from libs.config import GlobalConfig


class DoEndWork(object):
    """We did all the checks and works.
        Now closeup the and let's do the ending work
        """
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        
    def DoEndWork(self):
        """"""
        
        # save data
        self._save_local()
        
        check_report = self._gc.checks_done.get_check_report()
        if not check_report:
            return C.CHECK_OK
        
        err_presents = C.CHECK_OK
        for msgs in check_report:
            if isinstance(msgs, O.O_CheckReport):
                pass
            elif isinstance(msgs, O.O_UnhandledError):
                msg = "Disaster happens on: %s\n" % msgs.code_position
                msg += "".join(msgs.msg)
                self._gc.log.error(msg)
                err_presents = C.CHECK_ERROR
        
        return err_presents

    def _save_local(self):
        """"""
        lc = local_config.LocalConfig()
        lc.save(self._gc.local_config.check_data)
        
