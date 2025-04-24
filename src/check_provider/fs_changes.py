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
                            ("skip_hidden", (int, True)), 
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
        
        paths = [[], []]
        # walk thought address (path)
        for root, dirs, files in os.walk(self._address):
            # add root path
            paths[0].append(root)
            # we want only files, dirs will be present at future run os os.walk
            if not files:
                continue
            # add files to the path's list
            paths[1] += [os.path.join(root, p) for p in files if not self._skip_file(p)]
        
        return (C.CHECK_OK, paths)
    
    def _skip_file(self, file):
        """Return True if the file has to be skipped"""
        filename = os.path.basename(file)
        if self._host.specific_config.skip_hidden and filename.startswith("."):
            return True
        else:
            return False
    
    def handle_changes(self):
        """Indicate that we are able to handle changes"""
        return True
        
    def format_changes(self, old, new):
        """Format changes"""
        
        added_d, deleted_d = self._ctr_oldnew(old[0], new[0])
        added_f, deleted_f = self._ctr_oldnew(old[1], new[1])
        
        dta = ""
        
        if added_d: dta += "Added Dirs:\n+ %s\n\n" % "\n+ ".join(sorted(added_d))
        if deleted_d: dta += "Deleted Dirs:\n- %s\n\n" % "\n- ".join(sorted(deleted_d))
        
        if added_f: dta += "Added Files:\n+ %s\n\n" % "\n+ ".join(sorted(added_f))
        if deleted_f: dta += "Deleted Files:\n- %s\n\n" % "\n- ".join(sorted(deleted_f))

        return "Fs Change %s change content:\n%s\n" % (self._address, dta)
    
    def _ctr_oldnew(self, old, new):
        """Control for old and new files, return data splitted"""
        s_old = set()
        s_old.update(old)
        s_new = set()
        s_new.update(new)

        deleted = s_old.difference(s_new)
        added = s_new.difference(s_old)

        return added, deleted

    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_FsChange
