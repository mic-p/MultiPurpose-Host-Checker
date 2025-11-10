#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import smtplib
from email.message import EmailMessage
import email.utils as utils

from libs.config import GlobalConfig
from libs.report_msgs import check_build_msgs

class Evt_EmailSmtp(object):
    """"""
    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        
    def do_event(self, host_work):
        """"""
        event_name = host_work.check_work.host.on_event
        host_name = host_work.check_work.host.name
        smtp_config = self._gc.conf_event_handler[event_name]
        
        self._gc.log.debug("Send smtp email, Host: %s,  Via: %s, %s, to: %s" % (host_name, event_name,  smtp_config.smtp_host, smtp_config.address_to))
        
        # initialize connection to our email server
        try:
            smtp = smtplib.SMTP()
            smtp.connect(smtp_config.smtp_host or "localhost", port=smtp_config.smtp_port)
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
            msg_text = check_build_msgs(host_work.check_work)
                        
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
                    
        except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError) as err:
            msg_text = "SMTP server connection problems on server: '%s'" % smtp_config.smtp_host
            self._gc.log.error(msg_text)
            msg_text = (f"SMTP server {err=}, {type(err)=}")
            self._gc.log.error(msg_text)
            raise
            
        except smtplib.SMTPException:
            raise
        


def get_event_workers():
    return Evt_EmailSmtp
