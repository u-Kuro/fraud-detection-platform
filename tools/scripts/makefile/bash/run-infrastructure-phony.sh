#!/bin/bash
set -euo pipefail

MAKEFILE_PHONY="${1}"

WORKING_DIRECTORY=/app
HOST_UID="$(id -u)"
HOST_GID="$(id -g)"
DOCKER_RUN_ARGUMENTS=(
    --volume "${ROOT_DIRECTORY}:${WORKING_DIRECTORY}"
    --volume "${DOCKER_SOCK}:/var/run/docker.sock"
    --user "${HOST_UID}:${HOST_GID}"
)
if [[ -S /var/run/docker.sock ]]; then
    DOCKER_SOCK_GID="$(stat -c "%g" /var/run/docker.sock)"
    if [[ -n "${DOCKER_SOCK_GID}" ]]; then
        DOCKER_RUN_ARGUMENTS+=(--group-add "${DOCKER_SOCK_GID}")
    fi
fi

#echo "$PWD - here"
#cat /app/Makefile

set -x
docker run --rm \
    "${DOCKER_RUN_ARGUMENTS[@]}" \
    "${INFRASTRUCTURE_IMAGE}" \
    "make ${MAKEFILE_PHONY}"
set +x