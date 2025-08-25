# Roadmap
## Todo for v.1 (q4 2025)
- End wiki
- ~~End checks~~:
	- ~~dns_change~~ -> Done
	- ~~http_ok~~ -> Done (see to-do for evolutions and more infos)
	- ~~http_diff~~ -> Done
	- ~~restic_snapshots~~ -> Done
	- ~~fs_exists~~ -> Done
	- ~~fs_changes~~ -> Done

- Enable multiple checks and ~~multiple events handler for single host~~
- ~~Enable multiple records for dns_change for single check~~
- ~~Single host check via command line (-n, --host_check)~~

## Todo for v.2 (not planned)
- New checks:
	- Execute an external command and check the returncode. Example: verify the *MPHC* error logs and send email with the logs file has attachment

```
grep ERROR /var/log/mphc.log > /tmp/mphc_error.logs
```
- Linux .deb package
- Send email with attach

## Todo for v.3 (not planned)
- Linux systemd integration (code refactor)
- Thread code execution for checks (code refactor)
- Save events history into file / DB (Sqlite)

## Todo for v.4 (not planned)
- Office365 MFA email sender (Help need!)
