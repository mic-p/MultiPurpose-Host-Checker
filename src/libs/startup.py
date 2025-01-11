# -*- coding: UTF-8 -*-

import os,  sys
import argparse
import configparser

from libs.config import GlobalConfig
from libs.utils import  Singleton
from libs.log import Logging


class Startup(metaclass=Singleton):
    __doc__ = """"Startup function. Instance and call only the startup method"""
    def __init__(self):
        """"""
        self._startup_called = False
        self._startup_args = None
        self._gc = GlobalConfig()

    def startup(self):
        """"
        Default startup method that do all the first-time-execute work:
            - load all the data into config
            - ?
        """

        # if we have been already called, skip
        if self._startup_called:
            self._gc.log("Startup already called")
            return

        # parse startup args from sys.argv
        self._startup_args = self._parse()
        
        # load configuration
        self._load_conf_ini_global()
        self._load_config_hosts()
        
        self._gc.log = Logging()
        
        # at the end, check if all is ok
        self._startup_checks()
        
        self._gc.log("Startup done! Start to check hosts")
        self._gc.log.debug("Startup done! Start to check hosts")

        self._gc.startup_done = True

    def _load_conf_ini_global(self):
        """"""
        #start to load the configuration from
        config = configparser.ConfigParser()
        config.read(self._startup_args.config)

        self._gc.conf_mphc.debug = config.getint("default",  "debug",  fallback=0)
        self._gc.conf_mphc.continue_on_check_problem = config.getboolean("default",  "continue_on_check_problem",  fallback=1)
        self._gc.conf_mphc.path_data = config.get("default",  "path_data",  fallback="")
        
        # load configuration for logger
        _logger = config.get("logger", "logger")
        if _logger in ("syslog", "file"):
            self._gc.conf_log.logger = _logger
            if _logger == "syslog":
                _syslog_host = config.get("logger", "logger_syslog_host")
                if not _syslog_host:
                    self._gc.conf_log.logger_syslog_host = "/dev/log"
                else:
                    self._gc.conf_log.logger_syslog_host = _syslog_host
                    self._gc.conf_log.logger_syslog_port = config.get("logger", "logger_syslog_port") or 514
            else:
                self._gc.conf_log.logger_file = config.get("logger", "logger_file", fallback="")
        elif not _logger:
            self._gc.conf_log.logger = ""
        else:
            self._gc.conf_log.logger = config.getboolean("logger", "logger")

        # list of providers's configuration.
        # we create simply method for loading the .ini data with type and default values
        lst_startup_provider = (
                ("gmail_user",      ("get", "")),
                ("gmail_password",  ("get", "")),

                ("smtp_host",       ("get", "")),
                ("smtp_port",       ("getint", 25)),
                ("smtp_use_tls",    ("getboolean", False)),
                ("smtp_user",       ("get", "")),
                ("smtp_password",   ("get", "")),
        )

        for k, v in lst_startup_provider:
            fcall_str, fallback = v
            # load the function to load data (and type) from conf instance
            fcall = getattr(config, fcall_str)
            # set to the configuration the data loaded
            setattr(self._gc.conf_provider, k, fcall("logger", k, fallback=fallback))
        
    def _load_config_hosts(self):
        """"""
        config = configparser.ConfigParser()
        config.read(self._startup_args.hosts)

        self._gc.conf_mphc.execute_cmd_overall = config.get("default", "execute_cmd_overall",  fallback="")
        
    
    def _startup_checks(self):
        """Do startup check after configuration load"""
        
        if not  os.path.isdir(self._gc.conf_mphc.path_data):
            self._raise_err_exit("Path %s set into configuration is not a valid directory" % self._gc.conf_mphc.path_data, 3)
        
    
    def _raise_err_parse(self, parser, msg=""):
        """"""
        parser.print_help(sys.stderr)
        
        msg_err = "Error on argparse: %s" % str(msg)
        
        self._raise_err_exit(msg_err, 1)

    def _raise_err_exit(self, msg_err="", exit_code=1):
        """"""
        sys.stderr.write("%s\n\n" % msg_err)
        
        sys.exit(exit_code)

    def _parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-H", "--hosts", help="File where load hosts", type=str)
        parser.add_argument("-c", "--config", help="Configuration file", type=str)
        
        # scan args
        args = parser.parse_args()

        if not (args.hosts and args.config):
            self._raise_err_parse(parser, "No hosts or config file passed")
    
        # abs path of paths passed
        f1 = os.path.abspath(args.hosts)
        f2 = os.path.abspath(args.config)
        
        # check if file exists
        if not (os.path.exists(f1) and os.path.exists(f2)):
            self._raise_err_parse(parser, "No such file: %s or %s" % (f1, f2))

        return args
