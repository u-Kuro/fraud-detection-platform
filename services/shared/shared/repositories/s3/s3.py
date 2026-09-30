import boto3
from botocore.config import Config

s3_client = boto3.client(
    service_name="s3",
    config=Config(
        inject_host_prefix=False,
        request_checksum_calculation="when_required",
        s3={"addressing_style": "path"},
    )
)