import os

import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()
BUCKET = os.environ["S3_BUCKET"]

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["S3_ENDPOINT"],
    region_name=os.environ["S3_REGION"],
    aws_access_key_id=os.environ["S3_ACCESS_KEY"],
    aws_secret_access_key=os.environ["S3_SECRET_KEY"],
    config=Config(s3={"addressing_style": "path"}),
)

s3.put_object(
    Bucket=BUCKET,
    Key="deneme/merhaba.txt",
    Body="Merhaba nesne deposu!".encode("utf-8"),
    ContentType="text/plain; charset=utf-8",
)
print("Yüklendi")

liste = s3.list_objects_v2(Bucket=BUCKET, Prefix="deneme/")
for nesne in liste.get("Contents", []):
    print(nesne["Key"], nesne["Size"], "bayt")

cevap = s3.get_object(Bucket=BUCKET, Key="deneme/merhaba.txt")
print(cevap["Body"].read().decode("utf-8"))