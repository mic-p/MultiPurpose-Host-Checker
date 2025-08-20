# -*- coding: UTF-8 -*-

___doc___ = """ Configuration objects.
See mphc.conf.template and docs for explanations. Objs variables has the same names of the configurations keys.
"""

import libs.constants as C

class O_conf_mphc(object):
    """"""
    def __init__(self):
        """Genral MPHC configuration"""
        self.continue_on_check_problem = True
        self.execute_cmd_event_end = None
        self.execute_cmd_error_end = None
        
class O_conf_log(object):
    """Simple log configuration container"""
    def __init__(self):
        self.logger = None
        self.logger_file = None
        self.logger_syslog_host = ""
        self.logger_syslog_port = 514

    def __repr__(self):
        return "<O_conf_log>logger: %s, logger_file: %s" % (self.logger, self.logger_file)

class _BaseObj(object):
    """Base class for event handler"""
    def get_data_mandatory(self):
        """"""
        raise NotImplementedError
    
    def get_data_optional(self):
        """"""
        raise NotImplementedError

class _BaseDirObj(object):
    """Base obj that export the """
    def __dir(self):
        d = {}
        for x in self.__dict__:
            if not x.startswith("_"):
                d[x] = self.__dict__[x]
        return d
        
    def _repr(self):
        return ("; ".join(['%s: %s' % (key, value) for (key, value) in self.__dir().items()]))

class O_conf_event_handler_smtp(_BaseObj):
    """Simple event configuration container for smtp configuration"""
    __data_mandatory = (
                    ("type", (str, "")),
                    ("address_from", (str, "")),
                    ("address_to", (str, "")),
                )
    __data_optional =  (
                    ("smtp_host", (str, "")),
                    ("smtp_port", (int, 25)),
                    ("smtp_use_tls", (bool, False)),
                    ("smtp_user", (str, "")),
                    ("smtp_password", (str, "")),
                    ("email_subject", (str, "MPHC - Event")),
                )
    def __init__(self):
        super(O_conf_event_handler_smtp).__init__()
        """Set default variables"""
        self.smtp_host = ""
        self.smtp_port = 25
        self.smtp_use_tls = False
        self.smtp_user = ""
        self.smtp_password = ""

    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return  self.__data_optional

    def __repr__(self):
        return "<O_conf_event_handler_smtp>smtp_host: %s, smtp_user: %s" % (self.smtp_host, self.smtp_user)

class O_conf_event_handler_gmail(_BaseObj):
    """Simple event configuration container for gmail configuration"""
    __data_mandatory = (
                    ("type", (str, "")),
                    ("email_from", (str, "")),
                    ("email_to", (str, "")),
                    ("path_token", (str, "")),
                    ("path_credentials", (str, "")),
                )
    __data_optional = (
                    ("email_subject", (str, "MPHC - Event")),
        )

    def __init__(self):
        super(O_conf_event_handler_smtp).__init__()
        """Set default variables"""
        self.gmail_user = ""
        self.gmail_password = ""

    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional

    def __repr__(self):
        return "<O_conf_event_handler_gmail>gmail_user: %s" % (self.gmail_user, )

class O_conf_event_handler_cmd(_BaseObj):
    """Simple event configuration container for cmd configuration"""
    __data_mandatory = (
                            ("type", (str, "")),
                            ("execute_cmd",  (str, "")),
                        )
    __data_optional = ()

    def __init__(self):
        super(O_conf_event_handler_cmd).__init__()
        """Set default variables"""
        self.execute_cmd = ""

    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional

    def __repr__(self):
        return "<O_conf_event_handler_gmail>gmail_user: %s" % (self.gmail_user, )

class O_checks_done(object):
    """class that represent the events to handle.
    """
    def __init__(self):
        """"""
        self._checks_done = []
    
    def add_check(self, check):
        """"""
        self._checks_done.append(check)
    
    def get_check_report(self):
        """"""
        return [host for host in self._checks_done if host.check_work.report]

class O_check_work():
    """Object that represent a working check"""
    def __init__(self):
        """"""
        # our working host instance O_conf_host
        self.host = None
        
        # if != from CHECK_OK, we need to report it
        self.report = C.CHECK_OK
        # must be O_UnhandledError, O_CheckReport
        self.report_msg = None

class O_conf_specific_host(_BaseDirObj):
    """"""
    def __repr__(self):
        return "<O_conf_specific_host>data: %s" % self._repr()
    
class O_conf_host(_BaseObj):
    """Host configuration container"""
    __data_mandatory = (
                            ("check", (str, "")), 
                            ("on_event", (str, "")), 
                        )
    __data_optional = (
                            ("check_no_less_than", (str, "")), 
                            ("host_details_path", (str, "")), 
                            ("priority", (int, 0)), 
                        )
    def __init__(self):
        """"""
        self.name = ""
        self.check = ""
        self.on_event = ""
        self.host_details_path = ""
        self.host_details = []
        
        self.specific_config = O_conf_specific_host()
        
        self.check_toreport = False
        
    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional

    def __repr__(self):
        return "<O_conf_host>check: %s, on_event: %s" % (self.check, self.on_event)

class O_conf_host_detail(object):
    """Host configuration conteiner"""
    def __init__(self):
        """"""
        self.lst_hosts = []
        
    def __repr__(self):
        return "<O_conf_host_detail>lst_hosts: %s" % (self.lst_hosts, )

class O_event_handlers(dict):
    """Class that contain the events"""

class O_Hosts(dict):
    """Class that cointein the hosts"""

class O_UnhandledError(object):
    """Object that represent an unexpected error of the code"""
    def __init__(self, code_position, msg):
        """"""
        self.code_position = code_position
        self.msg = msg
    
    def format_error(self):
        """return formatted test of error"""
        return "Work state: %s\nError: %s" % (self.code_position, self.msg)
    
    def __repr__(self):
        """"""
        return "<O_UnhandledError>: %s" % self.msg

class O_CheckReport(object):
    """Object that represent a check report. Not error, only a message from a check to report"""
    
    def __init__(self, msg):
        """"""
        self.msg = msg
    
    def __repr__(self):
        """"""
        return "<O_CheckReport>: %s" % self.msg
        
class O_LocalConfig(object):
    """Configuration for the local configuration where every check can save data
        Every attribute will be saved with pickle
    """
    def __init__(self):
        """"""
        # seconds from the epoch of previous run
        self.previous_dt = 0
        
        # saved
        self.check_data = dict()
    

# Class that represent the types loaded from config
class T_AStr(object): pass
class T_AInt(object): pass
class T_AList(object): pass
    
