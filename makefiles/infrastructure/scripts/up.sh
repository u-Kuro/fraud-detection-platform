#!/bin/bash
set -euo pipefail

export TF_VAR_RUNNER_CONTAINER_NAME="${RUNNER_CONTAINER_NAME}"
export TF_VAR_HOST_USER="${HOST_USER-}"

terraform -chdir=infrastructure apply \
    -target="module.ministack_container.docker_container.ministack" \
    -auto-approve \
    -parallelism=1

terraform -chdir=infrastructure apply \
    -target="module.eks.data.external.k3s_configuration" \
    -auto-approve \
    -parallelism=1

terraform -chdir=infrastructure apply -auto-approve -parallelism=1