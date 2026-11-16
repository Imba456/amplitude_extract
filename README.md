# amplitude_extract
amplitude api extract section part of a larger pipeline.
including load section 

# Requirements
requirements amplitude for code flow

-----

# New repo
- [x] new repo
- [x] readme file
- [x] MIT license
- [x] git ignore > python
- [x] clone to local
- [x] create venv > `python -m venv .venv`
- [x] scripts activate > $ source .venv/Scripts/activate
- [x] python selector interpreter
- [x] new branch `git switch`
- [x] env file > API keys > check in git ignore
- [x] start sudo code execution
- [x] logging implemented
- [x] logging and data folders added to git ignore

-----

# sudo code plan
- [x] import os
- [x] import datetime
- [x] import requests #pip install requests
- [x] import json
- [x] import time
- [x] import logging
- [x] import zipfile
- [x] import gzip
- [x] import dotenv #pip install dotenv

- [x] start logging

- [x] timestamp for filename
- [x] create a data folder

- [ ]Update Extract script so that it checks S3 for what files have already been uploaded and calls the API for any missing data

- [x] while loop, 2 < max
    - [x] call API
    - [x] check the response
        - [x] if status code 2xx
            - [x] try - save data locally - except
            - [x] break
        - [x] elif status code 404 # no data
            - [x] break & log
        - [x] elif status code 403 # auth issue
            - [x] break & log
        - [x] elif status code 401 # auth malformed statement
            - [x] break & log
        - [x] elif status code 504 # rate limit hit
            - [x] #+=1
            - [x] wait 3600 seconds #unsure about this approach, rate limit resets in an hour but having an environment open for this long?
        - [x] else
            - [x] #+=1
            - [x] wait 30 seconds

- [x] save data locally

- [x] seperate py file for unpacking data
- [x] extract files
- [x] move files
- [x] rename files
- [x] link both python scripts so file names flow through
- [ ] unnest or fix JSON files if required

- [x] end logging


-----

# Git and requirements
- [ ] `pip freeze > requirements.txt`
- [ ] `git add .`
- [ ] `git commit -m "description"`

# monitor logging x
- [ ] consider notification steps

# load plan
loading from local to remote, S3 bucket, into snowflake
ETlT
- [x] create new branch
- [x] first comment plan
- [x] create s3 bucket
- [x] create s3 kms key
- [x] create aws roles
- [x] create aws policy
- [x] create aws user
- [x] create snowflake schema
- [x] create snowflake storage integration
- [x] create snowflake stage
- [x] create snowflake table for copy into
- [x] snowflake test copy into
- [x] commit mvp
- [x] commit dynamic logic
- [ ] go back to extract

# load sudo code
- [x] import aws related packages - boto3
- [x] import os
- [x] import dotenv
- [x] import logging

- [x] start logging
- [x] read in keys
- [x] where is json
- [x] create a list
- [x] connect to aws
- [x] setup s3 client

- [x] upload to s3
- [x] for loop
- [x] check the upload
- [x] delete locally
- [x] end logging