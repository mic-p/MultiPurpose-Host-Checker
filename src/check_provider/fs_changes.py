# -*- coding: UTF-8 -*-


class Check_Icmp(object):
    """"""
    __data_mandatory = (
                            #("", (str, "")),  
                        )
    __data_optional = (
                            ("fs_path", (int, 4)), 
                            #("", (str, "")), 
                        )
    def __init__(self):
        """"""

    def get_data_mandatory(self):
        """"""
        return self.__data_mandatory
    
    def get_data_optional(self):
        """"""
        return self.__data_optional


def get_check_workers():
    return Check_Icmp
