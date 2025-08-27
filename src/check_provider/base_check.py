# -*- coding: UTF-8 -*-

class BaseCheck(object):
    """Base class for event handler"""
    
    def do_check(self, *args, **kw):
        """"""
        # 
        if type(self).__bases__[0] is object:
            raise NotImplementedError
    
    def startup_config_checks(self, data):
        """Do startup configuration verification before start the work"""
    
    def startup_load(self, data):
        """Autonomous startup load of internal parameters"""
    
    def format_changes(self):
        """If the check handle changes, format them and return the informations"""
        return ""
    
    def handle_changes(self):
        """Does the check handle the changes from one run to the next?"""
        return False
    
    def get_data_mandatory(self):
        """Return the mandatory configuration data need by the check"""
        raise NotImplementedError
    
    def get_data_optional(self):
        """Return the optional configuration data need by the check"""
        raise NotImplementedError

    def set_uuid(self, work_uuid):
        """Set our unique work uuid"""
        self.__uuid = work_uuid
        
    def debug_log(self, msg):
        """"""
        self._gc.log.debug("%s-%s"% (self.__uuid,  msg, ))
