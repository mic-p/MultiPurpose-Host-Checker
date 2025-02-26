#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import smtplib
from email.message import EmailMessage
import email.utils as utils

from libs.config import GlobalConfig
import libs.constants as C

class Evt_EmailSmtp(object):
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        
    def do_event(self, host_work):
        """"""
        event_name = host_work.check_work.host.on_event
        smtp_config = self._gc.conf_event_handler[event_name]
        
        self._gc.log.debug("Send smtp email  via: %s, %s, to: %s" % (event_name,  smtp_config.smtp_host, smtp_config.address_to))
        
        # initialize connection to our email server
        smtp = smtplib.SMTP(smtp_config.smtp_host, port=smtp_config.smtp_port)

        smtp.ehlo()  # send the extended hello to our server
        if  smtp_config.smtp_use_tls:
            smtp.starttls()  # tell server we want to communicate with TLS encryption

        if smtp_config.smtp_user:
            smtp.login(smtp_config.smtp_user, smtp_config.smtp_password)  # login to our email server
        
        # create the email text message
        msg = EmailMessage()
        
        #remove the address part form email address and create the message-id
        domain = smtp_config.address_from.split("@")[1].strip().replace(">", "")
        msg['message-id'] = utils.make_msgid(domain=domain)
        
        # assemble text message
        if host_work.check_work.report == C.CHECK_ERROR:
            msg_text = "MPHC error\n--\n%s"
        elif host_work.check_work.report == C.CHECK_MSG:
            msg_text = "MPHC information reporting\n--\n%s"
        elif host_work.check_work.report == C.CHECK_DISASTER:
            msg_text = "MPHC disaster\n--\n%s"
        else:
            raise ValueError("Why here? %s" % host_work.check_work.report)
        
        msg_text = msg_text % host_work.check_work.report_msg.msg
        
        msg.set_content(msg_text)
        msg['subject'] = smtp_config.email_subject
        msg['to'] = smtp_config.address_to
        msg['from'] = smtp_config.address_from

        # send our email message 'msg' to our boss
        smtp.sendmail(smtp_config.address_from,
                      smtp_config.address_to,
                      msg.as_string()
                    )
                      
        smtp.quit()  # finally, don't forget to close the connection


def get_event_workers():
    return Evt_EmailSmtp
