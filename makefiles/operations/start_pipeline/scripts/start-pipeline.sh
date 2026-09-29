#!/bin/bash
set -euo pipefail

# Define data seed paths
TRANSACTION_INFERENCES_SEED_SOURCE="${ABSOLUTE_ROOT_DIRECTORY}/database/seed/transaction_inferences/creditcard_transactions.csv.gz"
TRANSACTION_INFERENCES_SEED_DESTINATION_KEY="fraud_detection_platform/data/seed/transaction_inferences/creditcard_transactions.csv.gz"

# Upsert seed for DAG workflow
aws s3 cp \
  "${TRANSACTION_INFERENCES_SEED_SOURCE}" \
  "s3://${S3_BUCKET}/${TRANSACTION_INFERENCES_SEED_DESTINATION_KEY}"

# Create temporary file for DAG call
temporary_file="$(mktemp)"
trap 'rm -f "${temporary_file}"' EXIT
cat > "${temporary_file}" <<EOF
{
  "logical_date": "2013-09-01T00:00:00Z",
  "conf": {
    "transaction_inferences_seed_s3_key": "${TRANSACTION_INFERENCES_SEED_DESTINATION_KEY}"
  }
}
EOF

# Get MWAA environment name
MWAA_ENVIRONMENT_NAME=$(
  aws ssm get-parameter \
    --name "/${PARAMETER_PATH}/mwaa/environment/name" \
    --query "Parameter.Value" \
    --output text
)

# Start the pipeline
aws mwaa invoke-rest-api \
  --name "${MWAA_ENVIRONMENT_NAME}" \
  --method POST \
  --path "/dags/cold_start/dagRuns" \
  --body "file://${temporary_file}"