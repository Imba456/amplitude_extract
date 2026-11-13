# Unzip and decompress files to retrieve .json files
# - Initial Unzip of 'amp_events.zip' is to a local 'data' folder
# - JSON files are extracted to this same folder

# Define Logging
import logging
from datetime import datetime

# Set Log filepath location
log_filename = f"logs/amplitude_load_unzip_folder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logs to retrieve INFO messages and higher
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger()

# Load libraries
import os
import zipfile
import gzip
import shutil
import tempfile

# Create a temporary directory for extraction
temp_dir = tempfile.mkdtemp()

# Create local output directory
data_dir = "datajson"
os.makedirs(data_dir, exist_ok=True)
logger.info("Environment Setup: beginning unzip process")

# test on initial file first before automating list
zippy = 'data/runtime 2026-11-13 10-14-47 datafrom 2026-11-12.zip'

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

print("All files extracted to the 'data' directory!")

logger.info('logger closed')