#!/bin/bash
set -euo pipefail

IMAGE="${1}"
MAKEFILE_TARGET="${2}"

WORKING_DIRECTORY=/app
HOST_UID="$(id -u)"
HOST_GID="$(id -g)"
DOCKER_RUN_ARGUMENTS=(
    --use-api-socket
    --network "host"
    --add-host "host.docker.internal:host-gateway"
    --add-host "api.host.docker.internal:host-gateway"
    --volume "${ABSOLUTE_ROOT_DIRECTORY}:${WORKING_DIRECTORY}"
    --user "${HOST_UID}:${HOST_GID}"
)
if [[ -S /var/run/docker.sock ]]; then
    DOCKER_SOCK_GID="$(stat -c "%g" /var/run/docker.sock)"
    if [[ -n "${DOCKER_SOCK_GID}" ]]; then
        DOCKER_RUN_ARGUMENTS=(
          "${DOCKER_RUN_ARGUMENTS[@]}"
          --group-add "${DOCKER_SOCK_GID}"
        )
    fi
fi

docker run -it --init --rm \
    "${DOCKER_RUN_ARGUMENTS[@]}" \
    "${IMAGE}" \
    "make ${MAKEFILE_TARGET}"