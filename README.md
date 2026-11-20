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

# 1. `events` (Core Event & Timestamp Fact Table)
Stores individual tracked actions, ingestion timestamps, and SDK routing metadata.

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `uuid` | `uuid` | UUID | **PK** — Unique event identifier |
| `insert_id` | `$insert_id` | String | Deduplication key |
| `insert_key` | `$insert_key` | String | Optional deduplication partition key (`null` in sample) |
| `schema_version` | `$schema` | Integer / String | Schema validation version (`null` in sample) |
| `event_id` | `event_id` | Integer | Sequential event counter per user/device |
| `event_type` | `event_type` | String | Name of the tracked event (e.g., `session_start`, `[Amplitude] Page Viewed`) |
| `amplitude_event_type` | `amplitude_event_type` | String | Internal system event override (`null` in sample) |
| `data_type` | `data_type` | String | Record classification (e.g., `event`) |
| `amplitude_id` | `amplitude_id` | Long | **FK** → `users.amplitude_id` |
| `session_id` | `session_id` | Long | **FK** → `sessions_devices.session_id` |
| `app` | `app` | Integer | Amplitude project/app ID (e.g., `100011471`) |
| `source_id` | `source_id` | String | Ingestion source identifier (`null` in sample) |
| `partner_id` | `partner_id` | String | Integration partner identifier (`null` in sample) |
| `is_attribution_event` | `is_attribution_event` | Boolean | Flag indicating an attribution-only event (`null` in sample) |
| `event_time` | `event_time` | Timestamp (UTC) | Amplitude-adjusted event timestamp |
| `client_event_time` | `client_event_time` | Timestamp (UTC) | Local device timestamp when event occurred |
| `client_upload_time` | `client_upload_time` | Timestamp (UTC) | Local device timestamp when batch uploaded |
| `server_received_time` | `server_received_time` | Timestamp (UTC) | Time Amplitude servers received the event |
| `server_upload_time` | `server_upload_time` | Timestamp (UTC) | Partition key used by Export API `start`/`end` |
| `processed_time` | `processed_time` | Timestamp (UTC) | Internal processing timestamp |
| `sample_rate` | `sample_rate` | Nullable / Float | Sampling rate applied (`null` in sample) |

---

# 2. `users` (User Identity & Profile Table)
Captures Amplitude's resolved user identity, advertising IDs, and account lifecycle timestamps.

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `amplitude_id` | `amplitude_id` | Long | **PK** — Amplitude's canonical internal user ID |
| `user_id` | `user_id` | String | Application external user ID (e.g., email, nullable) |
| `user_creation_time` | `user_creation_time` | Timestamp (UTC) | Timestamp when the user profile was first created (`null` in sample) |
| `paying` | `paying` | Boolean | Indicates whether the user has ever paid (`null` in sample) |
| `start_version` | `start_version` | String | App version on user's first recorded event (`null` in sample) |
| `amplitude_attribution_ids` | `amplitude_attribution_ids` | String | Attribution campaign/source identifiers (`null` in sample) |
| `adid` | `adid` | String | Google Advertising ID (`null` in sample) |
| `idfa` | `idfa` | String | Apple Identifier for Advertisers (`null` in sample) |

---

# 3. `sessions_devices` (Session, Device & Geolocation Context)
Groups hardware, browser/OS, SDK, and geographic context captured during a session.

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `session_id` | `session_id` | Long | **PK** — Session start timestamp in epoch ms (`-1` if out-of-session) |
| `amplitude_id` | `amplitude_id` | Long | **FK** → `users.amplitude_id` |
| `device_id` | `device_id` | String | Unique device/browser identifier |
| `device_family` | `device_family` | String | Broad device/OS family (e.g., `iOS`, `Windows`, `Linux`, `Other`) |
| `device_type` | `device_type` | String | Specific device/OS type (e.g., `Apple iPhone`, `Windows`) |
| `device_brand` | `device_brand` | String | Hardware brand (`null` in sample) |
| `device_manufacturer` | `device_manufacturer` | String | Hardware manufacturer (`null` in sample) |
| `device_model` | `device_model` | String | Hardware model code (`null` in sample) |
| `device_carrier` | `device_carrier` | String | Mobile network carrier (`null` in sample) |
| `platform` | `platform` | String | Platform name (e.g., `Web`) |
| `os_name` | `os_name` | String | Browser or OS name (e.g., `Mobile Safari`, `Chrome`) |
| `os_version` | `os_version` | String | Browser or OS version (e.g., `27`, `156`) |
| `version_name` | `version_name` | String | Application release version (`null` in sample) |
| `library` | `library` | String | Amplitude SDK name and version (e.g., `amplitude-ts/2.16.1`) |
| `language` | `language` | String | Device/browser locale language (e.g., `English`, `Japanese`) |
| `ip_address` | `ip_address` | String | Client IP address |
| `country` | `country` | String | Resolved country |
| `region` | `region` | String | Resolved state/province/region |
| `city` | `city` | String | Resolved city |
| `dma` | `dma` | String | Designated Market Area (e.g., `Buffalo, NY`) |
| `location_lat` | `location_lat` | Float | Latitude coordinate (`null` in sample) |
| `location_lng` | `location_lng` | Float | Longitude coordinate (`null` in sample) |

---

# 4. `event_properties` (Unnested Event Properties)
Key-value pairs extracted from `event_properties` (e.g., `[Amplitude] Page URL`, `[Amplitude] Page Counter`, `referrer`).

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `uuid` | `uuid` | UUID | **PK, FK** → `events.uuid` |
| `property_key` | `event_properties.<key>` | String | **PK** — Event property name |
| `property_value` | `event_properties.<value>` | String | String-cast property value |
| `value_type` | *Derived* | String | Original JSON type (`string`, `number`, `boolean`, `array`) |

---

# 5. `event_data` (Unnested Ingestion & System Metadata)
Flattened key-value pairs from the `data` object (e.g., `path: "/2/httpapi"`, `user_properties_updated: true`, `group_first_event`, `group_ids`).

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `uuid` | `uuid` | UUID | **PK, FK** → `events.uuid` |
| `data_key` | `data.<key>` | String | **PK** — Metadata field name |
| `data_value` | `data.<value>` | String | String-cast value (or JSON string for nested dicts like `group_ids`) |
| `value_type` | *Derived* | String | Original JSON type (`string`, `boolean`, `object`) |

---

# 6. `user_properties` (Unnested User & Attribution Properties)
Key-value pairs extracted from `user_properties` (and `global_user_properties` if populated), such as `initial_utm_source` and `initial_referrer`.

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `uuid` | `uuid` | UUID | **PK, FK** → `events.uuid` *(captures point-in-time user state on the event)* |
| `amplitude_id` | `amplitude_id` | Long | **FK** → `users.amplitude_id` |
| `scope` | *Derived* | String | **PK** — `project` (`user_properties`) or `global` (`global_user_properties`) |
| `property_key` | `user_properties.<key>` | String | **PK** — User property name |
| `property_value` | `user_properties.<value>` | String | String-cast property value (e.g., `EMPTY`) |
| `value_type` | *Derived* | String | Original JSON type (`string`, `number`, `boolean`, `array`) |

---

# 7. `event_groups` (Unnested Group Assignments)
Account or organization assignments extracted from `groups` (empty `{}` in sample).

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `uuid` | `uuid` | UUID | **PK, FK** → `events.uuid` |
| `group_type` | `groups.<key>` | String | **PK** — Group category name |
| `group_value` | `groups.<value>[i]` | String | **PK** — Specific group identifier (exploded if array) |

---

# 8. `event_group_properties` (Unnested Group Properties)
Custom attributes for associated groups extracted from `group_properties` (empty `{}` in sample).

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `uuid` | `uuid` | UUID | **PK, FK** → `events.uuid` |
| `group_type` | `group_properties.<group_type>` | String | **PK** — Group category name |
| `property_key` | `group_properties.<group_type>.<key>` | String | **PK** — Group property name |
| `property_value` | `group_properties.<group_type>.<value>` | String | String-cast group property value |
| `value_type` | *Derived* | String | Original JSON type (`string`, `number`, `boolean`, `array`) |

---

# 9. `event_plan` (Unnested Tracking Plan Metadata)
Tracking plan validation details extracted from `plan` (e.g., `branch`, `source`, `version`; empty `{}` in sample).

| Column | Source Field | Data Type | Key / Notes |
| :--- | :--- | :--- | :--- |
| `uuid` | `uuid` | UUID | **PK, FK** → `events.uuid` |
| `plan_key` | `plan.<key>` | String | **PK** — Tracking plan attribute (`branch`, `source`, `version`, `versionId`) |
| `plan_value` | `plan.<value>` | String | String-cast plan metadata value |