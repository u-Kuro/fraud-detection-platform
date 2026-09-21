#!/bin/bash
set -euo pipefail

terraform -chdir=infrastructure apply \
    -target="module.ministack_container.docker_container.ministack" \
    -auto-approve \
    -parallelism=1

terraform -chdir=infrastructure apply \
    -target="module.eks.data.external.k3s_configuration" \
    -auto-approve \
    -parallelism=1

terraform -chdir=infrastructure apply -auto-approve -parallelism=1