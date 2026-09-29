#!/bin/bash
set -euo pipefail

IMAGE_NAME="${1}"
RUNNER_CONTAINER_NAME="${2}"
COMMAND="${3}"

WORKING_DIRECTORY=/app
HOST_UID="$(id -u)"
HOST_GID="$(id -g)"
DOCKER_RUN_ARGUMENTS=(
    --use-api-socket
    --network "host"
    --add-host "host.docker.internal:host-gateway"
    --add-host "api.host.docker.internal:host-gateway"
    --volume "${ABSOLUTE_ROOT_DIRECTORY}:${WORKING_DIRECTORY}"
    --env RUNNER_CONTAINER_NAME="${RUNNER_CONTAINER_NAME}"
    --env HOST_USER="${HOST_UID}:${HOST_GID}"
    --user "${HOST_UID}:${HOST_GID}"
)

docker run -it --init --rm --name "${RUNNER_CONTAINER_NAME}" \
    "${DOCKER_RUN_ARGUMENTS[@]}" \
    "${IMAGE_NAME}" \
    "${COMMAND}"