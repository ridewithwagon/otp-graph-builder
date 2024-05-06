import boto3
import os
import io

s3 = boto3.client(
    service_name="s3",
    endpoint_url='https://689d872a37564a5d504b7236458b95ac.r2.cloudflarestorage.com',
    aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"),
    region_name="wnam",  # Must be one of: wnam, enam, weur, eeur, apac, auto
)

# Upload/Update single file
s3.upload_fileobj(io.BytesIO(
    open("graph.obj", "rb").read()
), "wagon-otp-graph", "graph.obj")
