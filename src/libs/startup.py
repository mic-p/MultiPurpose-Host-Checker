# -*- coding: UTF-8 -*-

import os,  sys
import argparse
import configparser

from libs.config import GlobalConfig
from libs.utils import  Singleton
from libs.log import Logging
from libs.utils import load_data_opt

from libs.objs import O_conf_event_handler_smtp, O_conf_event_handler_gmail, O_conf_event_handler_cmd, O_conf_host

import libs.check_handlers as check_handlers
import libs.event_handlers as event_handlers
import libs.local_config as local_config

class Startup(metaclass=Singleton):
    __doc__ = """"Startup function. Instance and call only the startup method"""
    def __init__(self):
        """"""
        self._startup_called = False
        self._startup_args = None
        self._gc = GlobalConfig()

    def DoStartupWork(self):
        """"
        Default startup method that do all the first-time-execute work:
            - load all the data into config
            - ?
        """

        # if we have been already called, skip
        if self._startup_called:
            self._gc.error("Startup already called")
            return
        
        # argparse instances
        self._mphc_global_config = None
        self._mphc_host_config = None
        
        # parse startup args from sys.argv
        self._startup_args = self._parse()
        
        # load configuration
        self._load_conf_ini_global()
        
        #startup logging
        self._gc.log = Logging()
        
        # startup check handlers
        self._checks_handler = check_handlers.CheckHandlers()
        self._checks_handler.load_checks_handlers()
        
        # startup event handlers
        self._event_handler = event_handlers.EventHandlers()
        self._event_handler.load_event_handlers()

        # load available check for all the controls
        self._available_checks = check_handlers.get_check_available()
        
        # load available event handler for all the controls
        self._available_event_handlers = event_handlers.get_event_available()
        
        # at the end, check if all is ok
        self._startup_checks()
        
        # load local configuration
        self._load_local_config()
        
        self._gc.startup_done = True
    
    def _load_local_config(self):
        """Load local saved data"""
        
        # load saved data on fs
        lc = local_config.LocalConfig()
        self._gc.local_config.check_data, self._gc.local_config.previous_dt = lc.load()
        
        for check_name in self._gc.hosts_config:
            self._gc.local_config.check_data.setdefault(check_name, None)
    
    def _load_conf_ini_global(self):
        """"""
        #start to load the configuration from
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(self._startup_args.config)
        
        #load global MPHC configuration
        # config, section, opt_name, ftype, fallback 
        self._gc.debug = load_data_opt(config, "global", "debug", int, 0)
        self._gc.conf_mphc.continue_on_check_problem = load_data_opt(config, "global", "continue_on_check_problem", bool, 1)
        self._gc.path_data = load_data_opt(config, "global", "path_data", str, "")
        self._gc.conf_mphc.execute_cmd_event_error = load_data_opt(config, "global", "execute_cmd_event_error", str, "")
        self._gc.conf_mphc.execute_cmd_global_error = load_data_opt(config, "global", "execute_cmd_global_error", str, "") 
        self._gc.conf_mphc.n_checks_simultaneously = load_data_opt(config, "global", "n_checks_simultaneously", int, 1) 
        
        # load configuration for logger, so the code can use it
        _logger = load_data_opt(config, "global",  "logger", str)
        if _logger in ("syslog", "file"):
            self._gc.conf_log.logger = _logger
            if _logger == "syslog":
                _syslog_host = load_data_opt(config, "global",  "logger_syslog_host", str)
                if not _syslog_host:
                    self._gc.conf_log.logger_syslog_host = "/dev/log"
                else:
                    self._gc.conf_log.logger_syslog_host = _syslog_host
                    self._gc.conf_log.logger_syslog_port = load_data_opt(config, "global", "logger_syslog_port", int, 514)
            else:
                self._gc.conf_log.logger_file = load_data_opt(config, "global", "logger_file", str)
        elif not _logger:
            self._gc.conf_log.logger = ""
        else:
            self._gc.conf_log.logger = _logger
            
        self._mphc_global_config = config

    def _startup_checks(self):
        """Do startup check after global configuration load"""

        self._load_event_handlers()
        self._load_config_hosts()

        if not  os.path.isdir(self._gc.path_data):
            msg = "Path %s set into configuration is not a valid directory" % self._gc.path_data
            self._gc.log.error(msg)
            self._raise_err_exit(msg, 3)

    def _load_event_handlers(self):
        """Load  checks from configuration"""
        # list of providers's configuration.
        # we create simply method for loading the .ini data with type and default values
        for sec_name in self._mphc_global_config.sections():
            #already loaded the global sec, skip it
            if sec_name == "global":
                continue
            # load type
            type_ = self._mphc_global_config[sec_name].get("type")
            if not type_ in self._available_event_handlers:
                raise ValueError("Value type %s of section %s not supported" % (type_,  sec_name))
            
            self._load_event_config(type_, sec_name)

    def _load_event_config(self, type_, section):
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
        
        #retrieve the right module handler for specific type_
        evt_handler_module = event_handlers.get_event_class(type_)
        self._gc.event_handles[section] = evt_handler_module

        self._gc.conf_event_handler[section] = Obj_event_handler
        
        data_mandatory, data_option = Obj_event_handler.get_data_mandatory(),  Obj_event_handler.get_data_optional()
        
        self._check_config_mandatory(self._mphc_global_config, section, data_mandatory)
        self._check_config_options(self._mphc_global_config, section, (data_mandatory,  data_option), ("type", ))
        
        self._set_data_config_obj(self._mphc_global_config, section, data_mandatory, Obj_event_handler)
        self._set_data_config_obj(self._mphc_global_config,section, data_option,  Obj_event_handler)
    
    def _check_config_mandatory(self, config, section, data):
        """Generic verification of the mandatory configuration"""
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
        """Verify if the options presents into the configuration are allowed"""
        exclude_check = exclude_check if exclude_check else ()
        opts_allowed = [x[0] for x in data[0]] + [x[0] for x in data[1]]
        
        for opt in config.options(section):
            if opt in exclude_check:
                continue
            if not opt in opts_allowed:
                msg = "Option %s present but not allowed in section %s" % (opt, section)
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
            valuetoset = load_data_opt(config, section, opt_name, ftype, fallback)
            setattr(obj_toset, opt_name, valuetoset)
            
    def _load_config_hosts(self):
        """Load host configuration into the specific objects"""
        
        # load configuration from files
        config = configparser.ConfigParser()
        config.read(self._startup_args.hosts)
        
        self._mphc_host_config = config
        
        # iterate over section and load configuration
        for sec_name in config.sections():
            self._load_check_host_config(sec_name)

    def _load_check_host_config(self, host_name):
        """Load for every hostname the config, controlling the data that came from config"""
        obj_host = O_conf_host()
        obj_host.name = host_name
                
        # verify if there is the "check" option into config
        if not "check" in self._mphc_host_config[host_name]:
            msg = "No such option check in: %s configuration" % host_name
            self._gc.log.error(msg)
            raise ValueError(msg)
        
        # and verify if we can handle the "check" option present
        check_name = self._mphc_host_config[host_name].get("check")
        if not check_name in self._available_checks:
            msg = "Check %s not available" % check_name
            self._gc.log.error(msg)
            raise ValueError(msg)
            
        # check if requested event exists
        on_event_data = self._mphc_host_config[host_name].get("on_event")
        if not on_event_data in self._gc.conf_event_handler:
            msg = "Event handler %s not available" % on_event_data
            self._gc.log.error(msg)
            raise ValueError(msg)

        # set the correct data
        obj_host.on_event = on_event_data
        obj_host.check = check_name
        
        # load hosts from secondary file
        host_details_path = self._mphc_host_config[host_name].get("host_details_path", fallback="")
        if host_details_path:
            if not os.path.exists(host_details_path):
                raise FileExistsError("No such file: %s" % host_details_path)
            with open(host_details_path) as host_details_path_f:
                obj_host.host_details = [line.strip() for line in host_details_path_f.readlines() if line and not line.strip().startswith("#")]
        
        self._gc.hosts_config[host_name] = obj_host
        
        # now check if the check configuration are valid
        self._load_check_config(obj_host, host_name, check_name)
    
    def _load_check_config(self, obj_host, host_name, check_name):
        """Load and check if the configuration are valid for specific check"""
        
        data_mandatory, data_option = obj_host.get_data_mandatory(),  obj_host.get_data_optional()

        # load data from checks
        checks = {}
        for cn in self._available_checks:
            checks[cn] = check_handlers.get_check_class(check_name).get_check_workers()

        # collect the generic mandatory+optional data for host plus the specific data that check needs
        data_mandatory_check = [x for x in data_mandatory] + [x for x in checks[check_name]().get_data_mandatory()]
        data_option_check = [x for x in data_option] + [x for x in checks[check_name]().get_data_optional()]
        # verify the mandatory configuration
        self._check_config_mandatory(self._mphc_host_config, host_name, data_mandatory_check)
        # and the optional one
        self._check_config_options(self._mphc_host_config, host_name, (data_mandatory_check,  data_option_check))

        # set the data into the obj configuration
        self._set_data_config_obj(self._mphc_host_config, host_name, data_mandatory_check, obj_host.specific_config)
        self._set_data_config_obj(self._mphc_host_config, host_name, data_option_check,  obj_host.specific_config)
        
        # leave the check verify the configuration, if need
        checks[check_name]().startup_config_checks(obj_host)
        
        # and load internal configuration, if need
        checks[check_name]().startup_load(obj_host)
        
    
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
