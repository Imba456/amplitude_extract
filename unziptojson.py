# Unzip and decompress files to retrieve .json files
# - Initial Unzip of 'amp_events.zip' is to a local 'data' folder
# - JSON files are extracted to this same folder
# Load libraries
import os
import zipfile
import gzip
import shutil
import tempfile
import logging
from datetime import datetime as dt

# Define Logging

timestamp = dt.now().strftime('%Y-%m-%d %H-%M-%S')
log_dir = 'logs/unzip'
os.makedirs(log_dir,exist_ok=True)
log_filename = f'{log_dir}/{timestamp}.log'

logging.basicConfig(
    filename = log_filename
    ,format = '%(asctime)s - %(levelname)s - %(message)s'
    ,level = logging.INFO
)

logger = logging.getLogger()
logger.info('logger initialised')

# Create a temporary directory for extraction
temp_dir = tempfile.mkdtemp()

# Create local output directory
data_dir = "datajson"
os.makedirs(data_dir, exist_ok=True)
logger.info("Environment Setup: beginning unzip process")

# test on initial file first before automating list
# zippy = 'data/runtime 2026-11-13 10-14-47 datafrom 2026-11-12.zip'

# run through the list next
zip_dir = "data"
file_list = os.listdir(zip_dir)

for file in file_list:
    zippy = f'{zip_dir}/{file}'
    print(zippy)
    try:
        # Extract the main zip file into the temporary directory
        with zipfile.ZipFile(zippy, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
            logger.info(f"{zipfile} extracted to temp directory: {temp_dir} ")
    except Exception as e:
        logger.error(f"Error extracting zip file: {str(e)}")
        raise

    try:
        # Locate the day folder (assumed to be the numeric folder)
        day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
        day_path = os.path.join(temp_dir, day_folder)
    except Exception as e:
        logger.error(f"Error finding day folder: {str(e)}")
        raise

    # Walk through the day folder and decompress each .gz file to the data directory
    for root, _, files in os.walk(day_path):
        for file in files:
            if file.endswith('.gz'):
                try:
                    gz_path = os.path.join(root, file)
                    json_filename = file[:-3]  # Remove .gz extension
                    output_path = os.path.join(data_dir, json_filename)

                    with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                        shutil.copyfileobj(gz_file, out_file)
                    
                    logger.info(f"Successfully processed: {file} -> {json_filename}")
                except Exception as e:
                    logger.error(f"Failed to process file {file}: {str(e)}")

    try:
        # Delete the temporary directory
        shutil.rmtree(temp_dir)
        logger.info("Temp directory deleted")

    except Exception as e:
        logger.error(f"Failed to delete temp directory: {str(e)}")

    print(f"All files from {zippy} extracted to the {data_dir} directory!")
    logger.info(f"All files from {zippy} extracted to the {data_dir} directory!")

logger.info('logger closed')