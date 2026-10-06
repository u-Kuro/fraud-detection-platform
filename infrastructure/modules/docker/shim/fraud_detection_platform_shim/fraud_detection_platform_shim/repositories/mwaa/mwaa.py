import boto3
from botocore.config import Config

def get_mwaa_client(endpoint_url: str):
    return boto3.client(
        service_name="mwaa",
        endpoint_url=endpoint_url,
        config=Config(
            inject_host_prefix=False,
            request_checksum_calculation="when_required",
        )
    )