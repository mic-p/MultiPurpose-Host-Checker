# -*- coding: UTF-8 -*-

class BaseCheck(object):
    """Base class for event handler"""
    
    def do_check(self, *args, **kw):
        """"""
        # 
        if type(self).__bases__[0] is object:
            raise NotImplementedError
                
    def get_data_mandatory(self):
        """"""
        raise NotImplementedError
    
    def get_data_optional(self):
        """"""
        raise NotImplementedError
