# -*- coding: UTF-8 -*-

___doc___ = """ Configuration objects.
See mphc.conf.template and docs for explanations. Objs variables has the same names of the configurations keys.
"""
class O_conf_mphc(object):
    """"""
    def __init__(self):
        """Genral MPHC configuration"""
        self.debug = False
        self.continue_on_check_problem = True
        self.execute_cmd_event_end = None
        self.execute_cmd_error_end = None
        self.path_data = ""
        

class O_conf_log(object):
    """Simple log configuration container"""
    def __init__(self):
        self.logger = None
        self.logger_file = None
        self.logger_syslog_host = ""
        self.logger_syslog_port = 514

    def __repr__(self):
        return "<O_conf_log>logger: %s, logger_file: %s" % (self.logger, self.logger_file)


class O_conf_event_handler_smtp(object):
    """Simple provider configuration container for smtp configuration"""

    def __init__(self):
        """Set default variables"""
        self.smtp_host = ""
        self.smtp_port = 25
        self.smtp_use_tls = False
        self.smtp_user = ""
        self.smtp_password = ""

    def __repr__(self):
        return "<O_conf_event_handler_smtp>smtp_host: %s, smtp_user: %s" % (self.smtp_host, self.smtp_user)

class O_conf_event_handler_gmail(object):
    """Simple provider configuration conteiner"""

    def __init__(self):
        """Set default variables"""
        self.gmail_user = ""
        self.gmail_password = ""

    def __repr__(self):
        return "<O_conf_event_handler_gmail>gmail_user: %s" % (self.gmail_user, )

class O_conf_host(object):
    """Host configuration container"""
    
    def __init__(self):
        """"""
        self.check = ""
        self.check_no_less_than = -1
        self.on_event = ""
        self.load_host_details = ""
        
    def __repr__(self):
        return "<O_conf_hosts>check: %s, on_event: %s" % (self.check, self.on_event)

class O_conf_host_detail(object):
    """Host configuration conteiner"""
    def __init__(self):
        """"""
        self.lst_hosts = []
        
    def __repr__(self):
        return "<O_conf_host_detail>lst_hosts: %s" % (self.lst_hosts, )
