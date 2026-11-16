from dotenv import load_dotenv
import os
import json
import boto3
import logging

load_dotenv()

#logging to be done

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
        os.remove(to_upload)
    except Exception as e:
        print(f'Something went wrong with the upload of {file}, Error: {e}')