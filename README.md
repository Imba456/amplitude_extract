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

# sudo code plan extract
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
EtLT
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

# sudo code load
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
- [x] end 


# Transform plan

planning potential questions we'd like to answer:
- [ ] What journeys are users taking on the website?
- [ ] Is a user making repeated clicks on the website? 
- [ ] Could this indicate a problem with the website?
- [ ] Can we flag any user behaviour that seems to indicate a problem with the website?
- [ ] Is there any evidence that a user finds the menu on the UK website confusing?
- [ ] Can we associate the IP address of a user with a particular company, so we can see which company is following us

planning json transform structure:
- [x] single event json identification
- [x] general user info in amplitude id
- [x] nested details in event_properties
- [x] event time, event type, ip address, region
- [x] user_properties
- [x] uuid unique event within a journey
- [x] event id follows a squence and continues from previous session to follow overall amplitude id interactions

design initial model schema for silver layer, upon creation, limit the tables and fields based on what our website supports

### 1. `silver_events` (Core Event, Session & Device Table)
Stores flattened top-level event, user, session, and device attributes sourced from `silver_stage`.

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `filename` | `bronze.filename` | VARCHAR | Source file name from ingestion *(note: needs to be added to `silver_stage`)* |
| `file_row_nr` | `bronze.file_row_nr` | INTEGER | Source row number within file *(note: needs to be added to `silver_stage`)* |
| `uuid` | `json:uuid` | VARCHAR | **PK** — Unique event identifier |
| `amplitude_id` | `json:amplitude_id` | BIGINT | Amplitude's canonical internal user ID |
| `app` | `json:app` | INT | Amplitude project/app ID |
| `city` | `json:city` | VARCHAR | Resolved city |
| `client_event_time` | `json:client_event_time` | TIMESTAMP_NTZ | Local device timestamp when event occurred |
| `client_upload_time` | `json:client_upload_time` | TIMESTAMP_NTZ | Local device timestamp when batch uploaded |
| `country` | `json:country` | VARCHAR | Resolved country |
| `data_type` | `json:data_type` | VARCHAR | Record classification (e.g., `event`) |
| `device_brand` | `json:device_brand` | VARCHAR | Hardware brand |
| `device_carrier` | `json:device_carrier` | VARCHAR | Mobile network carrier |
| `device_family` | `json:device_family` | VARCHAR | Broad device/OS family (e.g., `iOS`, `Windows`, `Linux`) |
| `device_id` | `json:device_id` | VARCHAR | Unique device/browser identifier |
| `device_manufacturer` | `json:device_manufacturer` | VARCHAR | Hardware manufacturer |
| `device_model` | `json:device_model` | VARCHAR | Hardware model code |
| `device_type` | `json:device_type` | VARCHAR | Specific device/OS type (e.g., `Apple iPhone`) |
| `dma` | `json:dma` | VARCHAR | Designated Market Area |
| `event_id` | `json:event_id` | INT | Sequential event counter per user/device |
| `event_time` | `json:event_time` | TIMESTAMP_NTZ | Amplitude-adjusted event timestamp (UTC) |
| `event_type` | `json:event_type` | VARCHAR | Name of the tracked event |
| `global_user_properties` | `json:global_user_properties` | VARIANT | Global user-level properties dictionary |
| `group_properties` | `json:group_properties` | VARIANT | Custom group-level properties dictionary |
| `idfa` | `json:idfa` | VARCHAR | Apple Identifier for Advertisers |
| `ip_address` | `json:ip_address` | VARCHAR | Client IP address |
| `is_attribution_event` | `json:is_attribution_event` | BOOLEAN | Flag indicating an attribution-only event |
| `language` | `json:language` | VARCHAR | Device/browser locale language |
| `library` | `json:library` | VARCHAR | Amplitude SDK name and version |
| `location_lat` | `json:location_lat` | FLOAT | Latitude coordinate |
| `location_lng` | `json:location_lng` | FLOAT | Longitude coordinate |
| `os_name` | `json:os_name` | VARCHAR | Browser or OS name |
| `os_version` | `json:os_version` | VARCHAR | Browser or OS version |
| `partner_id` | `json:partner_id` | VARCHAR | Integration partner identifier |
| `paying` | `json:paying` | BOOLEAN | Indicates whether the user has ever paid |
| `platform` | `json:platform` | VARCHAR | Platform name (e.g., `Web`) |
| `processed_time` | `json:processed_time` | TIMESTAMP_NTZ | Internal processing timestamp |
| `region` | `json:region` | VARCHAR | Resolved state/province/region |
| `sample_rate` | `json:sample_rate` | FLOAT | Sampling rate applied |
| `server_received_time` | `json:server_received_time` | TIMESTAMP_NTZ | Time Amplitude servers received the event |
| `server_upload_time` | `json:server_upload_time` | TIMESTAMP_NTZ | Time Amplitude servers uploaded the event |
| `session_id` | `json:session_id` | BIGINT | Session start timestamp in epoch ms (`-1` if out-of-session) |
| `source_id` | `json:source_id` | VARCHAR | Ingestion source identifier |
| `start_version` | `json:start_version` | VARCHAR | App version on user's first recorded event |
| `user_creation_time` | `json:user_creation_time` | TIMESTAMP_NTZ | Timestamp when the user profile was first created |
| `user_id` | `json:user_id` | VARCHAR | Application external user ID (nullable) |
| `user_properties` | `json:user_properties` | VARIANT | Raw user properties dictionary |
| `version_name` | `json:version_name` | VARCHAR | Application release version |

---

### 2. `silver_event_properties` (Unnested Event Properties)
Key-value pairs flattened from `silver_event_properties_stage.event_properties`.

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `uuid` | `silver_event_properties_stage.uuid` | VARCHAR | **PK, FK** → `silver_events.uuid` |
| `property_key` | `event_properties.<key>` | VARCHAR | **PK** — Event property name (e.g., `[Amplitude] Page URL`) |
| `property_value` | `event_properties.<value>` | VARCHAR | String-cast property value |

---

### 3. `silver_user_properties` (Unnested User Properties)
Key-value pairs flattened from `silver_user_properties_stage.user_properties`.

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `session_id` | `silver_user_properties_stage.session_id` | BIGINT | Session identifier associated with the event |
| `amplitude_id` | `silver_user_properties_stage.amplitude_id` | BIGINT | Amplitude canonical user ID *(note: aliased in stage view—see note below)* |
| `user_id` | `silver_user_properties_stage.user_id` | VARCHAR | External user ID *(note: missing from stage view—see note below)* |
| `property_key` | `user_properties.<key>` | VARCHAR | **PK** — User property name (e.g., `initial_utm_source`) |
| `property_value` | `user_properties.<value>` | VARCHAR | String-cast user property value |