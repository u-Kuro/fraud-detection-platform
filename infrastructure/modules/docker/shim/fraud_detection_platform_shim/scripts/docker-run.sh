#!/bin/bash
set -euo pipefail

IMAGE_NAME="${1}"
CONTAINER_NAME="${2}"
shift 2

DOCKER_RUN_ARGUMENTS=(
    --use-api-socket
    --network "host"
    --add-host "host.docker.internal:host-gateway"
    --volumes-from "${RUNNER_CONTAINER_NAME}"
)

if [[ -v HOST_USER ]]; then
    DOCKER_RUN_ARGUMENTS=(
        "${DOCKER_RUN_ARGUMENTS[@]}"
        --user "${HOST_USER}"
    )
fi

docker run -it --init --rm --name "${CONTAINER_NAME}" \
    "${DOCKER_RUN_ARGUMENTS[@]}" \
    "${IMAGE_NAME}" \
    "$@"