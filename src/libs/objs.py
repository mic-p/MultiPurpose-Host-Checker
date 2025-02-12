# -*- coding: UTF-8 -*-

___doc___ = """ Configuration objects.
See mphc.conf.template and docs for explanations. Objs variables has the same names of the configurations keys.
"""
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

class O_conf_event_handler_smtp(_BaseObj):
    """Simple event configuration container for smtp configuration"""
    __data_mandatory = ()
    __data_optional =  (
                ("smtp_host", (str, "")),
                ("smtp_port", (int, 25)),
                ("smtp_use_tls", (bool, False)),
                ("smtp_user", (str, "")),
                ("smtp_password", (str, "")),
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
    __data_mandatory = (("gmail_user",  (str, "")), ("gmail_password",  (str, "")))
    __data_optional = ()

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
    __data_mandatory = (("execute_cmd",  (str, "")), )
    __data_optional = ()

    def __init__(self):
        super(O_conf_event_handler_cmd).__init__()
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


class O_conf_specific_host(object):
    """"""

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
        
    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional

    def __repr__(self):
        return "<O_conf_hosts>check: %s, on_event: %s" % (self.check, self.on_event)

class O_conf_host_detail(object):
    """Host configuration conteiner"""
    def __init__(self):
        """"""
        self.lst_hosts = []
        
    def __repr__(self):
        return "<O_conf_host_detail>lst_hosts: %s" % (self.lst_hosts, )

class O_checks(dict):
    """Class that cointein the checks"""
        
class O_Hosts(dict):
    """Class that cointein the hosts"""
        
        
