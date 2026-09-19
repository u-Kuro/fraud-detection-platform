#!/bin/bash
set -euo pipefail

# Get inputs
query=$(cat)
main_network_name=$(printf "%s" "${query}"     | jq --raw-output '.main_network_name')
postgres_container_ip=$(printf "%s" "${query}" | jq --raw-output '.postgres_container_ip')

# Validate inputs values
validate_required() {
    local name="${1}" value="${2}"
    if [[ -z "${value//[[:space:]]/}" || "${value}" == "null" ]]; then
        echo "${name}: must be a non-empty string." 1>&2
        exit 1
    fi
}
validate_required "main_network_name"     "${main_network_name}"
validate_required "postgres_container_ip" "${postgres_container_ip}"

# Get main network configurations
main_network_json_configurations=$(docker inspect "${main_network_name}"    | jq '.[0]')
main_network_containers=$(printf "%s" "${main_network_json_configurations}" | jq '.Containers')

# Get Postgres container name using its IP in MiniStack network
postgres_container_name=$(
    printf "%s" "${main_network_containers}" \
    | jq --raw-output --arg ip "${postgres_container_ip}" \
    'first(to_entries[] | select((.value.IPv4Address // "") | startswith($ip + "/")) | .value.Name)'
)
if [[ -z "${postgres_container_name}" || "${postgres_container_name}" == "null" ]]; then
    echo "No container with IP '${postgres_container_ip}' found in network '${main_network_name}'." 1>&2
    exit 1
fi

# Get Postgres container configurations
postgres_container_json_configurations=$(docker inspect "${postgres_container_name}" | jq '.[0]')
postgres_container_ports=$(printf "%s" "${postgres_container_json_configurations}"   | jq '.NetworkSettings.Ports')

# Get Postgres container host port
postgres_container_host_port=$(printf "%s" "${postgres_container_ports}" | jq --raw-output 'to_entries[0].value[0].HostPort')
if [[ -z "${postgres_container_host_port}" || "${postgres_container_host_port}" == "null" ]]; then
    echo "'${postgres_container_name}' port has invalid value of '${postgres_container_host_port}'." 1>&2
    exit 1
fi

jq --null-input --compact-output \
    --arg postgres_container_host_port "${postgres_container_host_port}" \
    '{postgres_container_host_port: $postgres_container_host_port}'