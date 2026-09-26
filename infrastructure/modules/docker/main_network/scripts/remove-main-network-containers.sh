#!/bin/bash
set -euo pipefail

main_network_json_configurations=$(docker inspect "${MAIN_NETWORK_NAME}"    | jq '.[0]')
main_network_containers=$(printf "%s" "${main_network_json_configurations}" | jq '.Containers')

exclude_containers=(
  "ministack"
  "fraud_detection_platform_shim"
  "traefik_http_proxy"
)
while IFS= read -r container_name; do
    if [[ " ${exclude_containers[*]} " == *" ${container_name} "* ]]; then
        continue
    fi
    docker rm --force "${container_name}"
done < <(printf "%s" "${main_network_containers}" | jq --raw-output 'to_entries[] | .value.Name')