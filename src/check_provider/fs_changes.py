# -*- coding: UTF-8 -*-

import os

from libs.config import GlobalConfig
from .base_check import BaseCheck
from libs.objs import O_check_work

import libs.constants as C

class Check_FsChange(BaseCheck):
    """"""
    __data_mandatory = (
                            #("", (str, "")),  
                        )
    __data_optional = (
                            ("fs_path", (str, "")), 
                            #("", (str, "")), 
                        )
    def __init__(self):
        """"""
        super(Check_FsChange).__init__()
        self._gc = GlobalConfig()

        # class that represent our work
        self.check_work = O_check_work()
        
        self._host = None
        self._gc = GlobalConfig()
        
    def do_check(self, host, address):
        """"""
        self._address = address
        self._host = host
        self.check_work.host = host
        self._gc.log.debug("Start Fs Change check for: %s"% (host.name, ))
        
        if not os.path.exists(self._address):
            return (C.CHECK_MSG, "Fs Change, no such file or directory: %s" % self._address)
        
        paths = []
        # walk thought address
        for root, dirs, files in os.walk(self._address):
            # add root path
            paths.append(root)
            # we want only files, dirs will be present at future run os os.walk
            if not files:
                continue
            # add files to the path's list
            paths += [os.path.join(root, p) for p in files]
        
        return (C.CHECK_OK, paths)

    def handle_changes(self):
        """Indicate that we are able to handle changes"""
        return True
        
    def format_changes(self, old, new):
        """Format changes"""
        
        s_old = set()
        s_old.update(old)
        s_new = set()
        s_new.update(new)
        
        deleted = s_old.difference(s_new)
        added = s_new.difference(s_old)
        
        dta = "Added:\n+ %s\n\n" % "\n+ ".join(sorted(added))
        dta += "Deleted:\n- %s" % "\n- ".join(sorted(deleted))
        
        return "Fs Change %s change content:\n%s\n" % (self._address, dta)
        
    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_FsChange
