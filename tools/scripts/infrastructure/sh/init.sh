#!/bin/bash
set -euo pipefail

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

terraform init