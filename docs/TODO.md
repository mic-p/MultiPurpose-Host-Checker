# Version 1.0 blocking items

## code bugs / errors
- cleanup all the (old) unsued hosts from local saved file storage

## code todo
- end event cmd_execute (SMTP and GMAIL are ok)
- mphc.conf: handle global options ( execute_cmd_event_end, execute_cmd_error_end)
- host.conf: handle check_no_less_than,
- implement the possibility to read multiple values (array) from config, like:
	+ http_ok -> multiple ret code accepted
- http_ok:
	+ add port to connect to
	+ multiple ret code accepted
- restic_snapshots:
	+ accept --repository-file

## TODO list (sparse format)
- Documentation (wiki)
