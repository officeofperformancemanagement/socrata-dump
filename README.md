# socrata-dump

```
usage: socrata-dump [-h] [--compression COMPRESSION] [--file-size-limit FILE_SIZE_LIMIT] [--limit LIMIT] base outpath

Dump Socrata Data Portal Metadata and Assets into a Local Folder

positional arguments:
  base                  base url of Socrata instance
  outpath               output directory to save downloaded data

options:
  -h, --help            show this help message and exit
  --compression COMPRESSION
                        type of compression to apply to csv files. currently only valid value is "zip"
  --file-size-limit FILE_SIZE_LIMIT
                        total max file size in megabytes. any file larger than this will be deleted
  --limit LIMIT, -l LIMIT
                        total number of assets to process
```