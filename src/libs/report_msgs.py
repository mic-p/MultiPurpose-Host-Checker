# -*- coding: UTF-8 -*-

import libs.constants as C

def check_build_msgs(value):
    if value == C.CHECK_ERROR:
        msg_text = "MPHC error\n--\n%s"
    elif value == C.CHECK_MSG:
        msg_text = "MPHC information reporting\n--\n%s"
    elif value == C.CHECK_DISASTER:
        msg_text = "MPHC disaster\n--\n%s"
    else:
        raise ValueError("Why here? %s" % value)
    
    return msg_text
