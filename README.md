# amplitude_extract
amplitude api extract section part of a larger pipeline

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
- [ ] link both python scripts so file names flow through
- [ ] unnest or fix JSON files if required

- [ ] end logging


-----

# Git and requirements
- [ ] `pip freeze > requirements.txt`
- [ ] `git add .`
- [ ] `git commit -m "description"`

# monitor logging x
- [ ] consider notification steps