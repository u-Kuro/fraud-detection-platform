#!/bin/bash
set -euo pipefail

export TF_VAR_RUNNER_CONTAINER_NAME="${RUNNER_CONTAINER_NAME}"
export TF_VAR_HOST_USER="${HOST_USER-}"

terraform -chdir=infrastructure state rm \
    -backup="terraform.tfstate.backup" \
    module.exports \
    module.kyverno \
    module.metallb \
    module.mlflow \
    module.traefik \
    module.postgres \
    2>/dev/null || true

terraform -chdir=infrastructure destroy -auto-approve -parallelism=1 -refresh=false