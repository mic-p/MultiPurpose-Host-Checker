# -*- coding: UTF-8 -*-

# gmail email and process for auth2.0
# https://developers.google.com/gmail/api/quickstart/python
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from libs.config import GlobalConfig
from libs.report_msgs import check_build_msgs

import os

import base64
from email.message import EmailMessage

from googleapiclient.discovery import build

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", 'https://www.googleapis.com/auth/gmail.send']

class Evt_EmailGmail(object):
    """msg_text = "MPHC error reporting\n--\n%s" % host_work.check_work.error_msg
        msg.set_content(msg_text)
        msg['subject'] = smtp_config.email_subject
        msg['to'] = smtp_config.address_to
        msg['from'] = smtp_config.address_from

        # send our email message 'msg' to our boss
        smtp.sendmail(smtp_config.address_from,
                      smtp_config.address_to,
        """

    def __init__(self):
        """"""
        self._gc = GlobalConfig()
        
    def do_event(self, host_work):
        """"""
        self._host_work = host_work
        host_name = host_work.check_work.host.name
        event_name = host_work.check_work.host.on_event
        self._gmail_config = self._gc.conf_event_handler[event_name]
        self._gc.log.debug("Send gmail email for Host: %s with: %s to: %s" % (host_name, event_name, self._gmail_config.email_to, ))
        
        self._cred = self._check_credentials()
        self.SendMessage()
        
    def _check_credentials(self):
        """ check and return credentials
        https://developers.google.com/gmail/api/quickstart/python
        """
        path_credential = self._gmail_config.path_credentials
        path_token = self._gmail_config.path_token
        
        if not (os.path.exists(path_credential) or os.path.exists(path_token)):
            msg = "No such credential file exists or inaccessible: %s / %s\n. Exists!" % (path_credential, path_token)
            raise FileNotFoundError(msg)
        
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(path_token):
            creds = Credentials.from_authorized_user_file(path_token, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    path_credential, SCOPES
                )
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path_token, "w") as token:
            token.write(creds.to_json())

        return creds

    def SendMessage(self, attachmentFile=None):
        """Create and send an email message
            See: https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/send_message.py
        """
        sender = self._gmail_config.email_from
        to = self._gmail_config.email_to
        subject = self._gmail_config.email_subject
        host_work =  self._host_work
        
        # assemble text message
        msg_text = check_build_msgs(host_work.check_work)
        
        creds = self._cred

        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(msg_text)

        message["To"] = to
        message["From"] = sender
        message["Subject"] = subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        service.users().messages().send(userId="me", body=create_message).execute()
        

def get_event_workers():
    return Evt_EmailGmail

