# -*- coding: UTF-8 -*-

import os,  sys
import argparse
import configparser

from libs.config import GlobalConfig
from libs.utils import  Singleton
from libs.log import Logging

from libs.objs import O_conf_event_handler_smtp, O_conf_event_handler_gmail, O_conf_event_handler_cmd

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
        
        self._gc.log = Logging()
        
        # at the end, check if all is ok
        self._startup_checks()
        
        #self._gc.log("Startup done! Start to check hosts")
        self._gc.log.debug("Startup done! Start to check hosts")

        self._gc.startup_done = True

    def _load_conf_ini_global(self):
        """"""
        #start to load the configuration from
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(self._startup_args.config)

        self._gc.conf_mphc.debug = config.getint("default",  "debug",  fallback=0)
        self._gc.conf_mphc.continue_on_check_problem = config.getboolean("default",  "continue_on_check_problem",  fallback=1)
        self._gc.conf_mphc.path_data = config.get("default",  "path_data",  fallback="")
        self._gc.conf_mphc.execute_cmd_event_end = config.get("default", "execute_cmd_event_end",  fallback="")
        self._gc.conf_mphc.execute_cmd_error_end = config.get("default", "execute_cmd_error_end",  fallback="")
        
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
            
        self._config = config

    def _startup_checks(self):
        """Do startup check after global configuration load"""

        self._load_conf_ini_sections()
        self._load_config_hosts()

        if not  os.path.isdir(self._gc.conf_mphc.path_data):
            self._raise_err_exit("Path %s set into configuration is not a valid directory" % self._gc.conf_mphc.path_data, 3)


    def _load_conf_ini_sections(self):
        """load secondary sections"""
        # list of providers's configuration.
        # we create simply method for loading the .ini data with type and default values
        for sec_name in self._config.sections():
            if not sec_name.startswith("evth_"):
                continue
            type_ = self._config[sec_name].get("type")
            if not type_ in ("smtp", "gmail", "cmd"):
                raise ValueError("Value type %s of section %s not supported" % (type_,  sec_name))
            
            self._set_data_config(type_, sec_name)

    def _set_data_config(self, type_, section):
        """"""
        if type_ == "smtp":
            Obj_event_handler = O_conf_event_handler_smtp()
        elif type_ == "gmail":
            Obj_event_handler = O_conf_event_handler_gmail()
        elif type_ == "cmd":
            Obj_event_handler = O_conf_event_handler_cmd()
        else:
            raise ValueError("why here??? there is a BUG!")
    
        self._gc.conf_event_handler[section] = Obj_event_handler
        
        data_mandatory, data_option = Obj_event_handler.get_data_mandatory(),  Obj_event_handler.get_data_optional()
        
        self._check_config_mandatory(section, data_mandatory)
        self._check_config_options(section, (data_mandatory,  data_option), ("type", ))
        
        self._set_data_config_obj(section, data_mandatory, Obj_event_handler)
        self._set_data_config_obj(section, data_option,  Obj_event_handler)
    
    def _check_config_mandatory(self, section, data):
        """"""
        # retrieve only the option names. see __data_mandatory and __data_optional from objs
        opts_mandatory = [x[0] for x in data]
        # retrieve all the options into the section
        lst_options_present = self._config.options(section)
        for opt_m in opts_mandatory:
            if not opt_m in lst_options_present:
                msg = "No mandatory option set %s to section %s" % (opt_m, section)
                self._gc.log.error(msg)
                raise ValueError(msg)
                
    def _check_config_options(self, section, data,  exclude_check=None):
        """verify that option presents into the configuration are allowed"""
        exclude_check = exclude_check if exclude_check else ()
        opts_allowed = [x[0] for x in data[0]] + [x[0] for x in data[1]]
        
        for opt in self._config.options(section):
            if opt in exclude_check:
                continue
            if not opt in opts_allowed:
                msg = "Option %s presente but not allowed in section %s" % (opt, section)
                self._gc.log.error(msg)
                raise ValueError(msg)
    
    def _set_data_config_obj(self, section, data, obj_toset):
        """internal function that set attributes to the object passed, starting from:
            - config file instance
            - section
            - data to read from config file and to convert to the right type with default value if not present into the config file options
            - obj where set data
        """
        for opt_name, v in data:
            ftype, fallback = v
            # load the function to load data (and type) from conf instance
            if issubclass(ftype, int):
                fcall_str = "getint"
            elif issubclass(ftype, bool):
                fcall_str = "getboolean"
            elif issubclass(ftype, str):
                fcall_str = "get"
            else:
                raise ValueError("Type %s not supported" % str(ftype))
            
            # set to the configuration the data loaded.
            # here we use a workaround for a BUG of configparser that raise an exception when getint is called and the option is empty... argh!
            if fcall_str in ("getint", "getboolean") and self._config.get(section, opt_name) == "":
                    valuetoset = 0
            else:
                fcall = getattr(self._config, fcall_str)
                valuetoset = fcall(section, opt_name, fallback=fallback)
            setattr(obj_toset, opt_name, valuetoset)
            
    def _load_config_hosts(self):
        """"""
        config = configparser.ConfigParser()
        config.read(self._startup_args.hosts)
        

    
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
