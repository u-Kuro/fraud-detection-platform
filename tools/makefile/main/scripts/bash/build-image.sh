#!/bin/bash
set -euo pipefail

DOCKERFILE="${1}"
IMAGE="${2}"

docker build \
    --file "${DOCKERFILE}" \
    --tag "${IMAGE}" \
    "."