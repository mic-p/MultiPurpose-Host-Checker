# MultiPurpose-Host-Checker (MPHC)
*MPHC* is a simple and multipurpose host checker and monitoring program that helps you to control the behavior of your hosts.  

*MPHC* programs was developed with a simple rule in mind: users should take no more than four minutes to implement and use it.

## Features
- *MPHC* will monitor your hosts and notify you if anything changes or an event occurs
- Simply configurable with .ini file
- Works on Linux and Windows (and all the other platforms that runs Python)
- Extendible: do you know Python? You can write your checks and event handler following the templates included. In minutes without change the *MPHC* core code
- Production ready. *MPHC* was used for month in production for monitor company hosts

## Checks avaiables
- icmp: check with *ping* program the reachability of a host
- http_diff: check if one or more webpages is changed from last check
- http_ok: check if a webserver reply with status code 200
- fs_exists: check if a file or directory exists
- *other soon stay tuned or open a feature request*

## Event handler
- email_gmail: 
- email_smtp: 
- execute_cmd: 

## Documentation
- *MPHC* has only two configuration file:
	+ config.conf
	+ hosts.conf
- See wiki pages for more

## Why *MPHC* ?
- *MPHC* is not a complete monitoring system like Zabbix, Nagios or Solarwinds. No dashboards, graphs, trends, statistics are provided
- *MPHC* is just a software that checks your hosts with simplicity and alerts you

## Todo
- Linux systemd service integration
- Linux .deb package
- Office365 MFA email sender