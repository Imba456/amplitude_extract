from dotenv import load_dotenv
import os
import json
import boto3
import logging
from datetime import datetime as dt

load_dotenv()

#logging
timestamp = dt.now().strftime('%Y-%m-%d %H-%M-%S')
log_dir = 'logs/load'
os.makedirs(log_dir,exist_ok=True)
log_filename = f'{log_dir}/{timestamp}.log'

logging.basicConfig(
    filename = log_filename
    ,format = '%(asctime)s - %(levelname)s - %(message)s'
    ,level = logging.INFO
)

logger = logging.getLogger()

logger.info('logger initialised')

#check environment variables
aws_access_key = os.getenv('aws_access_key')
aws_secret = os.getenv('aws_secret')
s3_bucket = os.getenv('s3_bucket')

#initial check with hardcoded test files before switching to dynamic listing
# test_file = '100011471_2026-11-12_0#0.json'
# file_location = 'datajson/100011471_2026-11-12_0#0.json'

data_dir = 'datajson'
file_list = os.listdir(data_dir)

#setup s3 client
s3_client = boto3.client(
    's3'
    ,aws_access_key_id = aws_access_key
    ,aws_secret_access_key = aws_secret
)
#test upload to s3
# s3_client.upload_file(
#     file_location #local location
#     ,s3_bucket #the bucket
#     ,test_file #name of the file
# )

for file in file_list:
    to_upload = f'{data_dir}/{file}'
    try:
        s3_client.upload_file(
            to_upload
            ,s3_bucket
            ,file
        )
        print(f'{file} uploaded successfully')
        logger.info(f'{file} uploaded successfully')
        os.remove(to_upload)
        logger.info(f'{file} deleted locally')
    except Exception as e:
        print(f'Something went wrong with the upload of {file}, Error: {e}')
        logger.error(f'Something went wrong with the upload of {file}, Error: {e}')

logger.info('logger closed')