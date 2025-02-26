# SEND EMAIL WITH GMAIL

## Introduction
Bad news: Gmail (Google) phaseout basic authentication (user+pwd) from its services from 2021, forcing user to adopt more secure authentication mechanism like OAuth2

## MPHC and Gmail
Good news: *MPHC* full supports Gmail OAuth2!

## Usage
*MPHC* users that wants to send email with Gmail have to:
1) Create a Google Cloud project
2) Activate the APIs
3) Configure OAuth
	- Authorize the app for a Dekstop Usage
	- Download and save the *credentials.json* file
4) Configure *MPHC* to use *credentials.json*

See above references links for more information about the procedure to follow

## *MPHC* Startup for send email with Gmail

If you have downloaded the *credentials.json* from Google Cloud, save it to a conveniente path (we advices something like: *~/.config/google/credentials.json*)
After that, you have to warmup Google Cloud and login from the first time to Gmail service, creating the *token.json* file.  
*MPHC* have a convenient script that help you and tests the functionality.  

Look for *email_gmail_quickstart.py* inside the   
*$MPHC* *src/event_handler* directory and execute it:

```
user@server:~$ cd /opt/MPHC/src/event_handler
user@server:~$ python email_gmail_quickstart.py
```
Follow the istructions and enjoy!

## References
- https://support.google.com/a/answer/176600?hl=en
- https://developers.google.com/gmail/api/quickstart/python
