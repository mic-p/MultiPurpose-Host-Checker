# MultiPurpose-Host-Checker (MPHC)
*MPHC* is a program for monitor and check your Hosts in a MultiPurpose manner.  
*MPHC* helps you to control the behavior and the state of your hosts. It's up to you choose what and when *MPHC* will check your hosts.

*MPHC* programs was developed with a simple rule in mind: user should take no more than 4 (four) minutes to install and use it!

## Features
- Check your hosts and notify you if anything changes or an event occurs.
- Very simple configuration with .ini file
- Works on Linux and Windows (and all the other platforms that runs Python)
- Usable with cron (Linux) or Task Scheduler (Windows)
- Extendible: do you know Python? You can write your checks and event handler in minutes without change the *MPHC* core
- Production ready. *MPHC* was used for month in production for monitor company and internet hosts

## Checks avaiables
- icmp: check with *ping* program the reachability of a host
- http_diff: check if one or more webpages is changed from last check
- http_ok: check if a webserver reply with status code 200
- fs_exists: check if a file or directory exists and if not, alert
- fs_changes: 
- dns_change: 
- *other soon stay tuned or open a feature request*

## Event handler
- email_gmail: 
- email_smtp: 
- execute_cmd: 

## Installation
- download the .zip|.tar.gz file
- extract somewhere (/opt/mphc)
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
/opt/mphc/main.py

*That's all!*

## Documentation
- *MPHC* has only two configuration file:
	+ config.conf
	+ hosts.conf
- Both files are heavy commented and are auto-readble
- See wiki pages for more

## Why *MPHC* ?
- *MPHC* is not a complete monitoring system like Zabbix, Nagios or Solarwinds. No dashboards, graphs, trends, statistics are provided
- *MPHC* is just a software that checks your hosts with simplicity and alerts you when something happen

## Todo
- Linux systemd integration
- Linux .deb package
- Office365 MFA email sender
- Save events history into file / DB (Sqlite)