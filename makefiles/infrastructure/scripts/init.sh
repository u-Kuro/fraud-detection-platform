#!/bin/bash
set -euo pipefail

export TF_VAR_RUNNER_CONTAINER_NAME="${RUNNER_CONTAINER_NAME}"
export TF_VAR_HOST_USER="${HOST_USER-}"

terraform -chdir=infrastructure init