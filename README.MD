# INFO
[![BCH compliance](https://bettercodehub.com/edge/badge/nikolay-semenov/aws-s3-backup?branch=master)](https://bettercodehub.com/)
Simple script to copy a file (in this case, a file dump of redis database .rdb)

Locally, the script copies the file from one directory to another. 

After that, the script checks if the desired bucket is created, and if not, creates it.

Authorization data, local paths and the name of the bucket are set in config.ini
