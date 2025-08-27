# MultiPurpose-Host-Checker (MPHC)
*MPHC* is a program for monitor and Check your Hosts in a Multi Purpose manner.  
*MPHC* helps you to control the behavior and the state of your hosts. It's up to you choose what and when *MPHC* will check your hosts.

*MPHC* programs was developed with a simple rule in mind: user should take no more than 4 (four) minutes to install and use it!

## Features
- Check your hosts and notify you if anything changes or an event occurs.
- Very simple configuration with .ini style files
- Works on Linux and Windows (and all the other platforms that runs Python)
- Usable with cron (*nix) or Task Scheduler (Windows)
- Extendible: do you know Python? You can write your checks and event handler in minutes without change the *MPHC* core
- Production ready. *MPHC* is heavy tested for months in production environments to monitor company and internet hosts

## Checks avaiables
- icmp: check with *ping* program the reachability of a host
- http_diff: check if one or more webpages is changed from last check
- http_ok: check if a webserver reply with status code 200
- fs_exists: check if a file or directory exists and if not, alert
- fs_changes: check if someone modify your files
- dns_change: check if DNS record is changed from the last check
- restic_snapshots: verify if there is enought snapshots in the time period specified
- *other soon stay tuned or open a feature request*

## Event handler
- email_gmail: Send email with gmail. *MPHC* handle correctly OAuth2 protocol. See GMAIL readme for more details
- email_smtp: Send email via smtp protocol. See the documentations for more details
- execute_cmd: Execute a command. See the documentations for more details

## Installation
- See wiki pages for all the informations

## Documentation
- *MPHC* has only two configuration file:
	+ config.conf
	+ hosts.conf
- Both files are heavy commented and are auto-readble
- See wiki pages for more

## Why *MPHC* ?
- *MPHC* is a system that checks your hosts with simplicity and alerts you when something happen
- *MPHC* is not a complete monitoring system like Zabbix, Nagios or Solarwinds. No dashboards, graphs, trends, statistics are provided.

## Todo: see ROADMAP