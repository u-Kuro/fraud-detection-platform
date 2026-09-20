#!/bin/bash
set -euo pipefail

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