import boto3
from botocore.config import Config, _S3Dict

s3_client = boto3.client(
    service_name="s3",
    config=Config(
        inject_host_prefix=False,
        request_checksum_calculation="when_required",
        s3=_S3Dict(addressing_style="path"),
    )
)