# -*- coding: UTF-8 -*-

import libs.constants as C

def check_build_msgs(check_work):
    err = check_work.report
    if err == C.CHECK_ERROR:
        msg_text = "MPHC error\n--\n%s" % check_work.report_msg.format_error()
    elif err == C.CHECK_MSG:
        msg_text = "MPHC information reporting\n--\n%s" % check_work.report_msg.msg
    elif err == C.CHECK_DISASTER:
        msg_text = "MPHC disaster\n--\n%s"
    else:
        raise ValueError("Why here? %s" % err)
    
    return msg_text
