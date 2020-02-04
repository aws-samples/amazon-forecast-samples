Commands
========

The Makefile contains the central entry points for common tasks related to this project.

Syncing data to S3
^^^^^^^^^^^^^^^^^^

* `make sync_data_to_s3` will use `aws s3 sync` to recursively sync files in `data/` up to `s3://content-intelligence/outbrain/data/outbrain-daily-rev-RPM-2017.csv/data/`.
* `make sync_data_from_s3` will use `aws s3 sync` to recursively sync files from `s3://content-intelligence/outbrain/data/outbrain-daily-rev-RPM-2017.csv/data/` to `data/`.
