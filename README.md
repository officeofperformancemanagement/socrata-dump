# socrata-dump

```
usage: socrata-dump [-h] [--compression COMPRESSION] [--file-size-limit FILE_SIZE_LIMIT] [--key-id KEY_ID]
                    [--key-secret KEY_SECRET] [--limit LIMIT] [--provenance PROVENANCE]
                    base outpath

Dump Socrata Instance into a Folder, including both Metadata and Data

positional arguments:
  base                  base url of Socrata instance
  outpath               output directory to save downloaded data

options:
  -h, --help            show this help message and exit
  --compression COMPRESSION
                        type of compression to apply to csv files. currently only valid value is "zip"
  --file-size-limit FILE_SIZE_LIMIT
                        total max file size in megabytes. any file larger than this will be deleted
  --key-id KEY_ID       keyId for Socrata API
  --key-secret KEY_SECRET
                        keySecret for Socrata API
  --limit LIMIT, -l LIMIT
                        total number of assets to process
  --provenance PROVENANCE, -p PROVENANCE
                        filter by provenance: "community" or "official"
```