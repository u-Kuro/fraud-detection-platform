#!/bin/bash
set -euo pipefail

# Set default credentials
aws configure set aws_access_key_id     "${AWS_ACCESS_KEY_ID}"
aws configure set aws_secret_access_key "${AWS_SECRET_ACCESS_KEY}"

# Set default configurations
aws configure set region                       "${AWS_DEFAULT_REGION}"
aws configure set endpoint_url                 "${AWS_ENDPOINT_URL}"
aws configure set request_checksum_calculation "when_required"