import boto3
from botocore.config import Config

mwaa_client = boto3.client(
    service_name="mwaa",
    config=Config(
        inject_host_prefix=False,
        request_checksum_calculation="when_required",
    )
)