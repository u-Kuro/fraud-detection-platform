#!/bin/bash
set -euo pipefail

# Get inputs
query=$(cat)
main_network_name=$(printf "%s" "${query}"                        | jq --raw-output '.main_network_name')
main_network_gateway=$(printf "%s" "${query}"                     | jq --raw-output '.main_network_gateway')
airflow_container_url=$(printf "%s" "${query}"                    | jq --raw-output '.airflow_container_url')
airflow_requirements_file_path=$(printf "%s" "${query}"           | jq --raw-output '.airflow_requirements_file_path')
airflow_python_packages_constraint_url=$(printf "%s" "${query}"   | jq --raw-output '.airflow_python_packages_constraint_url')
kubeconfig_for_docker_file_path=$(printf "%s" "${query}"          | jq --raw-output '.kubeconfig_for_docker_file_path')
aws_configurations_for_docker_file_path=$(printf "%s" "${query}"  | jq --raw-output '.aws_configurations_for_docker_file_path')
aws_credentials_for_docker_file_path=$(printf "%s" "${query}"     | jq --raw-output '.aws_credentials_for_docker_file_path')

# Validate inputs values
validate_required() {
    local name="${1}" value="${2}"
    if [[ -z "${value//[[:space:]]/}" || "${value}" == "null" ]]; then
        echo "${name}: must be a non-empty string." 1>&2
        exit 1
    fi
}
validate_required "main_network_name"                       "${main_network_name}"
validate_required "main_network_gateway"                    "${main_network_gateway}"
validate_required "airflow_container_url"                   "${airflow_container_url}"
validate_required "airflow_requirements_file_path"          "${airflow_requirements_file_path}"
validate_required "airflow_python_packages_constraint_url"  "${airflow_python_packages_constraint_url}"
validate_required "kubeconfig_for_docker_file_path"         "${kubeconfig_for_docker_file_path}"
validate_required "aws_configurations_for_docker_file_path" "${aws_configurations_for_docker_file_path}"
validate_required "aws_credentials_for_docker_file_path"    "${aws_credentials_for_docker_file_path}"

# Get Airflow container IP
airflow_container_ip=$(printf "%s" "${airflow_container_url}" | sed -nE 's#^[^:]+://(\[[^]]+\]|[^:/?#]+).*#\1#p')

# Get main network configurations
main_network_json_configurations=$(docker inspect "${main_network_name}"    | jq '.[0]')
main_network_containers=$(printf "%s" "${main_network_json_configurations}" | jq '.Containers')

# Get Airflow container name using its IP in MiniStack network
airflow_container_name=$(
    printf "%s" "${main_network_containers}" \
    | jq --raw-output --arg ip "${airflow_container_ip}" \
    'first(to_entries[] | select((.value.IPv4Address // "") | startswith($ip + "/")) | .value.Name)'
)
if [[ -z "${airflow_container_name}" || "${airflow_container_name}" == "null" ]]; then
    echo "No container with IP '${airflow_container_ip}' found in network '${main_network_name}'." 1>&2
    exit 1
fi

# Get Airflow container configurations
airflow_container_json_configurations=$(docker inspect "${airflow_container_name}" | jq '.[0]')
airflow_container_ports=$(printf "%s" "${airflow_container_json_configurations}"   | jq '.NetworkSettings.Ports')
airflow_container_persisted_directory="/opt/airflow"
airflow_container_dag_directory_path="${airflow_container_persisted_directory}/dags"

# Install additional packages and dependencies in Airflow container
airflow_container_requirements_file_path="${airflow_container_persisted_directory}/requirements.txt"
docker exec "${airflow_container_name}" mkdir -p "${airflow_container_persisted_directory}" 1>/dev/null
docker cp "${airflow_requirements_file_path}" "${airflow_container_name}:${airflow_container_requirements_file_path}" 1>/dev/null
docker exec "${airflow_container_name}" sh -c "pip install -r '${airflow_container_requirements_file_path}' --constraint '${airflow_python_packages_constraint_url}' -qq" 1>/dev/null

# Copy kubeconfig to Airflow container for K3s access
airflow_container_kubeconfig_file_path="${airflow_container_persisted_directory}/kubeconfig.yaml"
docker exec "${airflow_container_name}" mkdir -p "${airflow_container_persisted_directory}" 1>/dev/null
docker cp "${kubeconfig_for_docker_file_path}" "${airflow_container_name}:${airflow_container_kubeconfig_file_path}" 1>/dev/null

# Set Airflow container AWS paths
airflow_user_home_aws_directory_path="/home/airflow/.aws"
airflow_container_aws_configurations_path="${airflow_user_home_aws_directory_path}/config"
airflow_container_aws_credentials_path="${airflow_user_home_aws_directory_path}/credentials"

# Initialize AWS config/credentials for Airflow's secrets backend (secrets manager)
docker exec "${airflow_container_name}" mkdir -p "${airflow_user_home_aws_directory_path}" 1>/dev/null
docker cp "${aws_configurations_for_docker_file_path}" "${airflow_container_name}:${airflow_container_aws_configurations_path}" 1>/dev/null
docker cp "${aws_credentials_for_docker_file_path}" "${airflow_container_name}:${airflow_container_aws_credentials_path}" 1>/dev/null

# Allow host.docker.internal for Linux OS (non-persistent)
docker exec "${airflow_container_name}" sh -c "echo '${main_network_gateway} host.docker.internal' >> /etc/hosts" 1>/dev/null

# Get Airflow container host port
airflow_container_host_port=$(printf "%s" "${airflow_container_ports}" | jq --raw-output 'to_entries[0].value[0].HostPort')
if [[ -z "${airflow_container_host_port}" || "${airflow_container_host_port}" == "null" ]]; then
    echo "'${airflow_container_name}' port has invalid value of '${airflow_container_host_port}'." 1>&2
    exit 1
fi

jq --null-input --compact-output \
    --arg airflow_container_name                 "${airflow_container_name}" \
    --arg airflow_container_host_port            "${airflow_container_host_port}" \
    --arg airflow_container_dag_directory_path   "${airflow_container_dag_directory_path}" \
    --arg airflow_container_kubeconfig_file_path "${airflow_container_kubeconfig_file_path}" \
    '{
        airflow_container_name:                 $airflow_container_name,
        airflow_container_host_port:            $airflow_container_host_port,
        airflow_container_dag_directory_path:   $airflow_container_dag_directory_path,
        airflow_container_kubeconfig_file_path: $airflow_container_kubeconfig_file_path
    }'