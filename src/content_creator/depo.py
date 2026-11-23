import os

import boto3
from botocore.config import Config

from content_creator import db  # noqa: F401  (.env'in yüklenmesi için)

BUCKET = os.environ["S3_BUCKET"]

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["S3_ENDPOINT"],
    region_name=os.environ["S3_REGION"],
    aws_access_key_id=os.environ["S3_ACCESS_KEY"],
    aws_secret_access_key=os.environ["S3_SECRET_KEY"],
    config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
)