# -*- coding: UTF-8 -*-

import os
import time
import pickle
from libs.config import GlobalConfig

STORE_PATH = "store.mphc"
LAST_RUN = "last_run.mphc"

class LocalConfig(object):
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        self._file_storage = os.path.join(self._gc.path_data, STORE_PATH)
        self._last_run = os.path.join(self._gc.path_data, LAST_RUN)

    def load(self):
        """"""
        if os.path.exists(self._file_storage):
            #data presents, load it
            with open(self._file_storage, 'rb') as f:
                # The protocol version used is detected automatically, so we do not
                # have to specify it.
                check_data = pickle.load(f)
        else:
            check_data = dict()
        
        if os.path.exists(self._last_run):
            #data presents, load it
            with open(self._last_run, 'rb') as f:
                # The protocol version used is detected automatically, so we do not
                # have to specify it.
                try:
                    previous_dt = int(f.read())
                except:
                    self._gc.log.error("Error opening: %s. Use default" % self._last_run)
                    previous_dt = 0
        else:
            previous_dt = 0
        
        return check_data, previous_dt
    
    def save(self, data):
        """Save data to local fs"""
        
        with open(self._file_storage, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

        with open(self._last_run, 'w') as f:
            # Save current time
            f.write("%i" % time.time())
            
            
