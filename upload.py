import logging
import os

import boto3

s3 = boto3.client(
    service_name="s3",
    endpoint_url='https://689d872a37564a5d504b7236458b95ac.r2.cloudflarestorage.com',
    aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
    region_name="wnam",  # Must be one of: wnam, enam, weur, eeur, apac, auto
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

available_files = os.listdir()
if 'graph.obj' not in available_files:
    logger.info("Available files:")
    for file in available_files:
        logger.info(file)
    logger.error("File graph.obj not found in current directory")
    exit(1)

file_size_mb = os.path.getsize('graph.obj') / 1024 / 1024
logger.info(f"Uploading file of size {file_size_mb:.2f} MB")

s3.upload_file('graph.obj', 'wagon-otp-graph', 'graph.obj')
