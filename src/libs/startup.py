# -*- coding: UTF-8 -*-

import os,  sys
import argparse
import configparser

from libs.config import GlobalConfig
from libs.utils import  Singleton
from libs.log import Logging

from libs.objs import O_conf_event_handler_smtp, O_conf_event_handler_gmail, O_conf_event_handler_cmd, O_conf_host
from check_provider import fs_exists, fs_changes, http_diff, http_ok, icmp

# to move to a better place and dynamic checks load
LST_EVENT_HANDLER = ("smtp", "gmail", "cmd")

# to move to a better place and dynamic checks load
LST_CHECKS = {"fs_exists": fs_exists ,
                        "fs_changes": fs_changes, 
                        "http_diff": http_diff,
                        "http_ok": http_ok,
                        "icmp": icmp}

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
        
        # argparse instances
        self._mphc_global_config = None
        self._mphc_host_config = None
        
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
        
        #load global MPHC configuration
        self._gc.debug = config.getint("global",  "debug",  fallback=0)
        self._gc.conf_mphc.continue_on_check_problem = config.getboolean("global",  "continue_on_check_problem",  fallback=1)
        self._gc.path_data = config.get("global",  "path_data",  fallback="")
        self._gc.conf_mphc.execute_cmd_event_end = config.get("global", "execute_cmd_event_end",  fallback="")
        self._gc.conf_mphc.execute_cmd_error_end = config.get("global", "execute_cmd_error_end",  fallback="")
        
        # load configuration for logger, so the code can use it
        _logger = config.get("global", "logger")
        if _logger in ("syslog", "file"):
            self._gc.conf_log.logger = _logger
            if _logger == "syslog":
                _syslog_host = config.get("global", "logger_syslog_host")
                if not _syslog_host:
                    self._gc.conf_log.logger_syslog_host = "/dev/log"
                else:
                    self._gc.conf_log.logger_syslog_host = _syslog_host
                    self._gc.conf_log.logger_syslog_port = config.get("logger", "logger_syslog_port") or 514
            else:
                self._gc.conf_log.logger_file = config.get("global", "logger_file", fallback="")
        elif not _logger:
            self._gc.conf_log.logger = ""
        else:
            self._gc.conf_log.logger = config.getboolean("global", "logger")
            
        self._mphc_global_config = config

    def _startup_checks(self):
        """Do startup check after global configuration load"""

        self._load_mphc_checks()
        self._load_config_hosts()

        if not  os.path.isdir(self._gc.path_data):
            self._raise_err_exit("Path %s set into configuration is not a valid directory" % self._gc.path_data, 3)


    def _load_mphc_checks(self):
        """Load  checks from configuration"""
        # list of providers's configuration.
        # we create simply method for loading the .ini data with type and default values
        for sec_name in self._mphc_global_config.sections():
            #already loaded the global sec, skip it
            if sec_name == "global":
                continue
            # load type
            type_ = self._mphc_global_config[sec_name].get("type")
            if not type_ in LST_EVENT_HANDLER:
                raise ValueError("Value type %s of section %s not supported" % (type_,  sec_name))
            
            self._set_mphc_global_data_config(type_, sec_name)

    def _set_mphc_global_data_config(self, type_, section):
        """"""
        # check the type and instance the correct event
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
        
        self._check_config_mandatory(self._mphc_global_config, section, data_mandatory)
        self._check_config_options(self._mphc_global_config, section, (data_mandatory,  data_option), ("type", ))
        
        self._set_data_config_obj(self._mphc_global_config, section, data_mandatory, Obj_event_handler)
        self._set_data_config_obj(self._mphc_global_config,section, data_option,  Obj_event_handler)
    
    def _check_config_mandatory(self, config, section, data):
        """"""
        # retrieve only the option names. see __data_mandatory and __data_optional from objs
        opts_mandatory = [x[0] for x in data]
        # retrieve all the options into the section
        lst_options_present = config.options(section)
        for opt_m in opts_mandatory:
            if not opt_m in lst_options_present:
                msg = "No mandatory option set %s to section %s" % (opt_m, section)
                self._gc.log.error(msg)
                raise ValueError(msg)
                
    def _check_config_options(self, config, section, data,  exclude_check=None):
        """verify that option presents into the configuration are allowed"""
        exclude_check = exclude_check if exclude_check else ()
        opts_allowed = [x[0] for x in data[0]] + [x[0] for x in data[1]]
        
        for opt in config.options(section):
            if opt in exclude_check:
                continue
            if not opt in opts_allowed:
                msg = "Option %s presente but not allowed in section %s" % (opt, section)
                self._gc.log.error(msg)
                raise ValueError(msg)
    
    def _set_data_config_obj(self, config, section, data, obj_toset):
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
            if fcall_str in ("getint", "getboolean") and config.get(section, opt_name) == "":
                    valuetoset = 0
            else:
                fcall = getattr(config, fcall_str)
                valuetoset = fcall(section, opt_name, fallback=fallback)
            setattr(obj_toset, opt_name, valuetoset)
            
    def _load_config_hosts(self):
        """"""
        # load data from checks
        for check_name in LST_CHECKS:
            self._gc.checks[check_name] = LST_CHECKS[check_name].get_check_workers()
        
        # load configuration from files
        config = configparser.ConfigParser()
        config.read(self._startup_args.hosts)
        
        self._mphc_host_config = config
        
        # iterate over section and load coniguration
        for sec_name in config.sections():
            self._set_host_data_config(sec_name)

    def _set_host_data_config(self, host_name):
        """"""
        obj_host = O_conf_host()
        
        data_mandatory, data_option = obj_host.get_data_mandatory(),  obj_host.get_data_optional()
        
        # verify if there is the "check" option into config
        if not "check" in self._mphc_host_config[host_name]:
            msg = "No such option check in: %s connfiguration" % host_name
            self._gc.log.error(msg)
            raise ValueError(msg)
        
        # and verify if we can handle the "check" option present
        check_name = self._mphc_host_config[host_name].get("check")
        if not check_name in LST_CHECKS:
            msg = "Check %s not available" % check_name
            self._gc.log.error(msg)
            raise ValueError(msg)
            
        # verify mandatory and option data for host plus the specific data that check needs
        data_mandatory_check = [x for x in data_mandatory] + [x for x in self._gc.checks[check_name]().get_data_mandatory()]
        data_option_check = [x for x in data_option] + [x for x in self._gc.checks[check_name]().get_data_optional()]
        
        #verify the mandatory configuration
        self._check_config_mandatory(self._mphc_host_config, host_name, data_mandatory_check)
        #and the optional one
        self._check_config_options(self._mphc_host_config, host_name, (data_mandatory_check,  data_option_check))
        
        # check if event exists
        on_event_data = self._mphc_host_config[host_name].get("on_event")
        if not on_event_data in self._gc.conf_event_handler:
            msg = "Event handler %s not available" % on_event_data
            self._gc.log.error(msg)
            raise ValueError(msg)
        
        # set the data into the obj configuration
        self._set_data_config_obj(self._mphc_host_config, host_name, data_mandatory, obj_host)
        self._set_data_config_obj(self._mphc_host_config, host_name, data_option,  obj_host)
        
        self._gc.hosts_config[host_name] = obj_host
        
    def _raise_err_parse(self, parser, msg=""):
        """parse error, exit please"""
        parser.print_help(sys.stderr)
        msg_err = "Error on argparse: %s" % str(msg)
        self._raise_err_exit(msg_err, 1)

    def _raise_err_exit(self, msg_err="", exit_code=1):
        """raise and exit with exit code"""
        sys.stderr.write("%s\n\n" % msg_err)
        sys.exit(exit_code)

    def _parse(self):
        """parse startup args"""
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
