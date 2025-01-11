# -*- coding: UTF-8 -*-

class O_conf_mphc(object):
    """"""
    def __init__(self):
        """"""
        self.debug = False
        self.execute_cmd_overall = False
        self.continue_on_check_problem = True
        
        self.path_data = ""
        

class O_conf_log(object):
    """Simple log configuration conteiner"""
    def __init__(self):
        self.logger = None
        self.logger_file = None
        self.logger_syslog_host = ""
        self.logger_syslog_port = 514

    def __repr__(self):
        return "<O_conf_log>logger: %s, logger_file: %s" % (self.logger, self.logger_file)


class O_conf_provider(object):
    """Simple provider configuration conteiner"""

    def __init__(self):
        """Set default variables"""
        self.gmail_user = ""
        self.gmail_password = ""
        self.smtp_host = ""
        self.smtp_port = 25
        self.smtp_use_tls = False
        self.smtp_user = ""
        self.smtp_password = ""

    def __repr__(self):
        return "<O_conf_log>gmail_user: %s, smtp_host: %s, smtp_user: %s" % (self.gmail_user, self.smtp_host, self.smtp_user)

class O_conf_host(object):
    """Host configuration conteiner"""
    
    def __init__(self):
        """"""
        self.check = ""
        self.check_no_less_than = -1
        
        self.on_event = ""
        
        self.execute_cmd = ""
        
        self.load_host_details = ""
        
        
    def __repr__(self):
        return "<O_conf_hosts>logger: %s, logger_file: %s" % (self.logger, self.logger_file)

class O_conf_host_detail(object):
    """Host configuration conteiner"""
    def __init__(self):
        """"""
        self.lst_hosts = []
        
