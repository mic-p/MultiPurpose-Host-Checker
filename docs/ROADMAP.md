# Roadmap
## Todo for v.1 (q4 2025)
- End wiki
- ~~End checks~~:
	- ~~dns_change~~ -> Done
	- ~~http_ok~~ -> Done
	- ~~http_diff~~ -> Done
	- ~~restic_snapshots~~ -> Done
	- ~~fs_exists~~ -> Done
	- ~~fs_changes~~ -> Done

- ~~Enable multiple records for dns_change for single check~~
- ~~Single host check via command line (-n, --host_check)~~
- ~~Enable the cmd_execute event handler~~
- ~~Debug overwrite via command line~~
- ~~Handle execute_cmd_global_error~~
- ~~host.conf: handle check_no_less_than~~

## Todo for v.2 (not planned)
- Enable multiple checks and multiple events handler for single host
- Update fs_changes for handle the file moves (now MPHC reports delete+add)
- New checks:
	- socket check: test for open port(s)
	- SSL/TLS check: verify if the specific host reply with SSL/TLS
	- Execute an external command and check the returncode. Example: verify the *MPHC* error logs and send email with the logs file has attachment. Something like:
```
grep ERROR /var/log/mphc.log > /tmp/mphc_error.logs
```
- Linux .deb package
- Send email with attachments

## Todo for v.3 (not planned)
- Linux systemd integration (code refactor)
- Save events history into file / DB (Sqlite)
- ~~Thread code execution for checks (code refactor)~~

## Todo for v.4 (not planned)
- Office365 MFA email sender (Help needed!)
