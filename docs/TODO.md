# Version 1.0 blocking items

## code bugs / errors
- cleanup all the (old) unsued hosts from local saved file storage

## code todo
- end event cmd_execute (SMTP and GMAIL are ok)
- host_details_path -> load addressed from file
- do remain checks
- mphc.conf: handle global options ( execute_cmd_event_end, execute_cmd_error_end)
- host.conf: handle check_no_less_than,
- implement the possibility to read multiple values (array) from config, like:
	+ httpok -> multiple ret code accepted
- httpok:
	+ port to connect to
	+ multiple ret code accepted
- on restic_snapshots:
	- accepted only S3 and local repository, do all the code work for accept via mhpc.conf and env vars:
		+ Azure Blob
		+ Google Cloud Storage
		+ rclone
		+ sftp
		+ rest
		+ OpenStack Swift
		+ B2
	- accept --repository-file

## TODO list (sparse format)
- Documentation (wiki)
