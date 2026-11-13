import os
from datetime import datetime as dt
from datetime import timedelta as td
import requests
import json
import time
import logging
import zipfile
import gzip
from dotenv import load_dotenv as lde

timestamp = dt.now().strftime('%Y-%m-%d %H-%M-%S')

#print(timestamp)

log_dir = 'logs'
os.makedirs(log_dir,exist_ok=True)
log_filename = f'{log_dir}/{timestamp}.log'

logging.basicConfig(
    filename = log_filename
    ,format = '%(asctime)s - %(levelname)s - %(message)s'
    ,level = logging.INFO
)

logger = logging.getLogger()
logger.info('logger initialised')


#construct api call for yesterday
base_api_endpoint = 'https://analytics.eu.amplitude.com/api/2/export'
dttoday = dt.today()
dtyesterday = dttoday - td(days=1)
start_time = dtyesterday.strftime('%Y%m%dT00')
end_time = dtyesterday.strftime('%Y%m%dT23')
api_endpoint = f'{base_api_endpoint}?start={start_time}&end={end_time}'

print(api_endpoint)
logger.info(f'api end point constructed: {api_endpoint}')

data_dir = 'data'
timestamp_datafrom = dtyesterday.strftime('%Y-%m-%d')
os.makedirs(data_dir,exist_ok=True)
filename = f'{data_dir}/runtime {timestamp} datafrom {timestamp_datafrom}.zip'

#load api info https://amplitude.com/docs/apis/analytics/export
#docs mention base64 encoding, requests seems to handle that itself
lde()
key = os.getenv('AMP_API_KEY')
secret = os.getenv('AMP_SECRET_KEY')



attempts = 0
max_attempts = 2

while attempts <= max_attempts:

    response = requests.get(api_endpoint,auth=(key,secret))
    status_code = response.status_code

    if 200<=status_code<300:
        try:

            with open(filename,'wb') as file:
                file.write(response.content) #currently no safeguarding around having no response, so files can be empty if there is no response

            print(f'file {filename} saved successfully 👍')
            logger.info(f'file {filename} saved successfully 👍')

        except Exception as e:
            print(f"an error occurred when saving the zip file: {e}")
            logger.error(f"an error occurred when saving the zip file: {e}")

        break

    elif status_code==404:
        print(f'API call failed, status code {status_code}, no data in range 🤬')
        logger.error(f'API call failed, status code {status_code}, no data in range 🤬')
        break

    elif status_code==403:
        print(f'API call failed, status code {status_code}, auth issue 🤬')
        logger.error(f'API call failed, status code {status_code}, auth issue 🤬')
        break
    elif status_code==504:
        print(f'API call failed, status code {status_code}, rate limit reached 🤬')
        logger.error(f'API call failed, status code {status_code}, rate limit reached 🤬')
        if attempts==max_attempts:
            print(f'max attempts reached')
            logger.warning(f'max attempts reached')
        else:
            print(f'Attempt {attempts} failed status code {status_code}, waiting 1h before the next attempt')
            logger.error(f'Attempt {attempts} failed status code {status_code}, waiting 1h before the next attempt')
            attempts+=1
        time.sleep(3600) #unsure about this approach, rate limit resets in an hour but having an environment open for this long?
    else:
        if attempts==max_attempts:
            print(f'max attempts reached')
            logger.warning(f'max attempts reached')
        else:
            print(f'Attempt {attempts} failed status code {status_code}, waiting 30 seconds before the next attempt')
            logger.error(f'Attempt {attempts} failed status code {status_code}, waiting 30 seconds before the next attempt')
        attempts+=1
        time.sleep(30)

logger.info('logger closed')