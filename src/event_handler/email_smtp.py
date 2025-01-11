#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import smtplib

class event_raised():
    
    # initialize connection to our email server, we will use Outlook here
    smtp = smtplib.SMTP('smtp-mail.outlook.com', port='587')

    smtp.ehlo()  # send the extended hello to our server
    smtp.starttls()  # tell server we want to communicate with TLS encryption

    smtp.login('joe.bloggs@outlook.com', 'Password123')  # login to our email server

    # send our email message 'msg' to our boss
    smtp.sendmail('joe.bloggs@outlook.com',
                  'joes.boss@outlook.com',
                  msg.as_string())
                  
    smtp.quit()  # finally, don't forget to close the connection

def provider():
    return event_raised
