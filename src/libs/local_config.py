# -*- coding: UTF-8 -*-

import os
import time
import pickle


import libs.constants as C
from libs.config import GlobalConfig

class LocalConfig(object):
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        self._file_storage = os.path.join(self._gc.path_data, C.PATH_CHECK_DATA)
        self._last_run = os.path.join(self._gc.path_data, C.PATH_LAST_RUN)
        self._last_run_check = os.path.join(self._gc.path_data, C.PATH_LAST_RUN_CHECK)

    def load(self):
        """Load from local saved data path"""
        
        # load data
        check_data = self._load_pickle(self._file_storage)
        last_run_check = self._load_pickle(self._last_run_check)
        previous_dt = self._load_dt(self._last_run)
        
        self._startup_data(check_data, last_run_check)
        
        return check_data, last_run_check, previous_dt
    
    def _startup_data(self, check_data, last_run_check):
        """create if necessary a default key for every host in local data"""
        for check_name in self._gc.hosts_config:
            check_data.setdefault(check_name, None)
            last_run_check.setdefault(check_name, 0)
    
    def _load_dt(self, path):
        """Load the DT into path passed, otherwise create an empty one"""
        if os.path.exists(path):
            #data presents, load it
            with open(path, 'rb') as f:
                try:
                    previous_dt = int(f.read())
                except:
                    self._gc.log.error("Error opening: %s. Use default" % self._last_run)
                    previous_dt = 0
        else:
            previous_dt = 0
        
        return previous_dt
        
    
    def _load_pickle(self, path):
        """Load the path passed with pickle, otherwise create an empty one"""

        if os.path.exists(path):
            #data presents, load it
            with open(path, 'rb') as f:
                # The protocol version used is detected automatically, so we do not
                # have to specify it.
                data = pickle.load(f)
        else:
            data = dict()
        
        return data

    def _cleanup_hosts(self):
        """Cleanup the local configuration from non existing hosts"""
        
    def save(self, data_storage, data_last_run_check):
        """Save data to local fs"""
        
        save_hosts = [h for h in data_storage]
        h_to_remove = [h for h in save_hosts if not h in self._gc.hosts_config]
        for h in h_to_remove:
            data_storage.pop(h)
            data_last_run_check.pop(h)
        
        self._save_pickle(self._file_storage, data_storage)
        self._save_pickle(self._last_run_check, data_last_run_check)

        with open(self._last_run, 'w') as f:
            # Save current time
            f.write("%i" % time.time())
            
    def _save_pickle(self, path, data):
        """Save the data into the path with pickle"""
        with open(path, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            try:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
            except:
                print(data)
                raise
