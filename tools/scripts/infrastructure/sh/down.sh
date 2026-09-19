#!/bin/bash
set -euo pipefail

if [[ ${#} -ne 4 ]]; then
    echo "Usage: ${0} <SHELL_CMD> <SCRIPT_EXTENSION> <SCRIPT_FLAG> <COMMAND_FLAG>" 1>&2
    exit 1
fi
SHELL_CMD="${1}"
SCRIPT_EXTENSION="${2}"
SCRIPT_FLAG="${3}"
COMMAND_FLAG="${4}"

location_pushed=false
cleanup() {
    if $location_pushed; then
        popd 1>/dev/null
    fi
}
trap cleanup EXIT

if [[ "${PWD##*/}" != "infrastructure" ]]; then
    pushd infrastructure 1>/dev/null
    location_pushed=true
fi

export TF_VAR_SHELL_CMD="${SHELL_CMD}"
export TF_VAR_SCRIPT_EXTENSION="${SCRIPT_EXTENSION}"
export TF_VAR_SCRIPT_FLAG="${SCRIPT_FLAG}"
export TF_VAR_COMMAND_FLAG="${COMMAND_FLAG}"

terraform state rm \
    -backup="terraform.tfstate.backup" \
    module.exports \
    module.kyverno \
    module.metallb \
    module.mlflow \
    module.traefik \
    module.postgres \
    2>/dev/null || true

terraform destroy -auto-approve -parallelism=1 -refresh=false