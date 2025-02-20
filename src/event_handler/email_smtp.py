#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import smtplib
from email.message import EmailMessage
import email.utils as utils

from libs.config import GlobalConfig

class EmailSmtp(object):
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
        msg_text = "MPHC error reporting\n--\n%s" % host_work.check_work.error_msg
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
    return EmailSmtp
