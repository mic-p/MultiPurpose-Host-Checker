# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# https://developers.google.com/gmail/api/quickstart/python

# [START gmail_quickstart]
import sys
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", 'https://www.googleapis.com/auth/gmail.send']


def main():
    """Shows basic usage of the Gmail API.
      Lists the user's Gmail labels.
    """
    
    # [START MPHC code]
    path_token = os.path.expanduser("~/.config/google/token.json") 
    path_credential = os.path.expanduser("~/.config/google/credentials.json") 
    if len(sys.argv) != 3:
        print("No input file for token and creds passed. I'm using: '%s' and '%s'" % (path_token, path_credential))
        val = input("Continue? [Y|N] ").strip()
        if not val in "Yy":
            print ("Exit")
            return
    else:
        path_token, path_credential = sys.argv[1:]
    creds = None
    # [END MPHC code]
    
    #  [START gmail_quickstart]
    """
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """
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

    try:
    # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])
        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(label["name"])
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

if __name__ == "__main__":
  main()
# [END gmail_quickstart]
