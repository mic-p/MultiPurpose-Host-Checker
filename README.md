# MultiPurpose-Host-Checker (MPHC)
*MPHC* is a program for monitor and check your Hosts in a MultiPurpose manner.  
*MPHC* helps you to control the behavior and the state of your hosts. It's up to you choose what and when *MPHC* will check your hosts.

*MPHC* programs was developed with a simple rule in mind: user should take no more than 4 (four) minutes to install and use it!

## Features
- Check your hosts and notify you if anything changes or an event occurs.
- Very simple configuration with .ini style files
- Works on Linux and Windows (and all the other platforms that runs Python)
- Usable with cron (Linux) or Task Scheduler (Windows)
- Extendible: do you know Python? You can write your checks and event handler in minutes without change the *MPHC* core
- Production ready. *MPHC* was heavy tested for month in production for monitor company and internet hosts

## Checks avaiables
- icmp: check with *ping* program the reachability of a host
- http_diff: check if one or more webpages is changed from last check
- http_ok: check if a webserver reply with status code 200
- fs_exists: check if a file or directory exists and if not, alert
- fs_changes: check if someone modify your files
- dns_change: check if DNS record is changed from the last check
- *other soon stay tuned or open a feature request*

## Event handler
- email_gmail: Send email with gmail. *MPHC* handle correctly OAuth2 protocol. See GMAIL readme for more details
- email_smtp: Send email. See the documentations for more details
- execute_cmd: Execute a command. See the documentations for more details

## Installation
- download the .zip|.tar.gz file
- extract somewhere (/opt/MPHC)
- copy configuration templates file from /opt/mphc/template to somewhere (/etc/mphc)
- edit:
	+ mphc.conf
	+ hosts.conf
- test it
```
# has simple as

$ unzip mhpc.zip | tar xzf mphc.zip
$ mv mphc /opt/mphc
$ mkdir /etc/mphc
$ cp /opt/mphc/* /etc/mphc
$ nano|vi /etc/mphc/*
$ chmod +rx /opt/mphc/main.py
$ ln -s /opt/mphc/main.py /usr/local/bin/mphc

$ mphc -c /etc/mphc/mphc.conf -H /etc/mphc/hosts.conf
```

*That's all!*

## Documentation
- *MPHC* has only two configuration file:
	+ config.conf
	+ hosts.conf
- Both files are heavy commented and are auto-readble
- See wiki pages for more

## Why *MPHC* ?
- *MPHC* is not a complete monitoring system like Zabbix, Nagios or Solarwinds. No dashboards, graphs, trends, statistics are provided.
- *MPHC* is just a software that checks your hosts with simplicity and alerts you when something happen

## Todo: see ROADMAP