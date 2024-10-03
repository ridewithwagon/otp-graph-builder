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


def upload_if_exists(file_name):
    if file_name in available_files:
        file_size_mb = os.path.getsize(file_name) / 1024 / 1024
        logger.info(f"Uploading {file_name} of size {file_size_mb:.2f} MB")

        s3.upload_file(file_name, 'wagon-otp-graph', file_name)
    else:
        logger.info(f"File {file_name} not found")


upload_if_exists("streetGraph.obj")
upload_if_exists("graph.obj")
