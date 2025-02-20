# Roadmap
## Todo for v.1 (q2 2025)
- End wiki
- End checks:
	+ http_diff
	+ http_ok
	+ fs_exists
	+ fs_changes
	+ dns_change
- Enable multiple checks and multiple events handler
- Enable multiple records for dns_change

## Todo for v.2 (not planned)
- New checks:
	+ Execute an external command and check the returncode. Example: verify the *MPHC* error logs and send email with the logs file has attachment

```
grep ERROR /var/log/mphc.log > /tmp/mphc_error.logs
```
- Linux .deb package

## Todo for v.3 (not planned)
- Linux systemd integration (code refactor)
- Save events history into file / DB (Sqlite)

## Todo for v.4 (not planned)
- Office365 MFA email sender (Help need!)
