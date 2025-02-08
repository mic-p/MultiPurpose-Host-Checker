
from libs.utils import  Singleton

import logging
import logging.handlers

from logging.handlers import RotatingFileHandler

from .config import GlobalConfig

LOG_FORMAT = '%(name)s: %(levelname)s %(message)s'
#LOG_FORMAT = "%(asctime)s %(name)s %(message)s"

class Logging(metaclass=Singleton):
    """"""

    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        
        logger = logging.getLogger("MPHC")
        
        # set debug level has request by the conf
        if self._gc.conf_mphc.debug:
            ll = logging.DEBUG
        else:
            ll = logging.INFO
        logger.setLevel(ll)
        
        if self._gc.conf_log.logger == "syslog":
            if self._gc.conf_log.logger_syslog_host.startswith("/"):
                address = self._gc.conf_log.logger_syslog_host
            else:    
                address = (self._gc.conf_log.logger_syslog_host, self._gc.conf_log.logger_syslog_port)
            handler = logging.handlers.SysLogHandler(address = address)
            
        elif self._gc.conf_log.logger == "file":
            # add a rotating handler
            handler = RotatingFileHandler(self._gc.conf_log.logger_file, maxBytes=1024 * 1024,
                backupCount=3,
                encoding='utf-8')
        logger.addHandler(handler)
        
        handler.setFormatter(logging.Formatter(LOG_FORMAT))

        self._log = logger

    def log(self, *args):
        self._write(*args)
    def error(self, *args):
        self._write(*args, error=1)
    def exception(self, *args):
        self._write(*args, exception=1)
    def debug(self, *args):
        self._write(*args, debug=1)

    def _write(self, *args, **kw):
        """"""
        # log funct need only one arg, write it alone
        if len(args) == 1:
            v = args[0]
        else:
            v = ";".join([str(x) for x in args])
        
        # info this log
        #print (v)
        if "debug" in kw:
            f_log = self._log.debug
        elif "exception" in kw:
            f_log = self._log.exception
        elif "error" in kw:
            f_log = self._log.error
        else:
            f_log = self._log.info
        f_log(v)
        
        #self._log.handlers[0].flush()

    def __call__(self, *args):
        """"""
        self.log(*args)
