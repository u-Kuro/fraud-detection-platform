#!/bin/bash
set -euo pipefail

trap 'cd "${ABSOLUTE_ROOT_DIRECTORY}"' EXIT

paths=(
    "dags"
    "infrastructure/modules/docker/shim/fraud_detection_platform_shim"
    "notebooks"
    "services"
)
for path in "${paths[@]}"; do
    cd "${ABSOLUTE_ROOT_DIRECTORY}/${path}"

    uv sync --all-packages --all-groups
done