#!/bin/bash
set -euo pipefail

# Get inputs
query=$(cat)
main_network_name=$(printf "%s" "${query}"                  | jq --raw-output '.main_network_name')
eks_cluster_endpoint=$(printf "%s" "${query}"               | jq --raw-output '.eks_cluster_endpoint')
k3s_registries_file_path=$(printf "%s" "${query}"           | jq --raw-output '.k3s_registries_file_path')
kubeconfig_for_localhost_file_path=$(printf "%s" "${query}" | jq --raw-output '.kubeconfig_for_localhost_file_path')
kubeconfig_for_docker_file_path=$(printf "%s" "${query}"    | jq --raw-output '.kubeconfig_for_docker_file_path')

# Validate inputs values
validate_required() {
    local name="${1}" value="${2}"
    if [[ -z "${value//[[:space:]]/}" || "${value}" == "null" ]]; then
        echo "${name}: must be a non-empty string." 1>&2
        exit 1
    fi
}
validate_required "main_network_name"                  "${main_network_name}"
validate_required "eks_cluster_endpoint"               "${eks_cluster_endpoint}"
validate_required "k3s_registries_file_path"           "${k3s_registries_file_path}"
validate_required "kubeconfig_for_localhost_file_path" "${kubeconfig_for_localhost_file_path}"
validate_required "kubeconfig_for_docker_file_path"    "${kubeconfig_for_docker_file_path}"

# Get main network configurations
main_network_json_configurations=$(docker inspect "${main_network_name}"    | jq '.[0]')
main_network_containers=$(printf "%s" "${main_network_json_configurations}" | jq '.Containers')

# Get EKS endpoint host and port
eks_endpoint_host=$(printf "%s" "${eks_cluster_endpoint}" | sed -nE 's#^[^:]+://(\[[^]]+\]|[^:/?#]+).*#\1#p')
eks_endpoint_port=$(printf "%s" "${eks_cluster_endpoint}" | sed -nE 's#^[^:]+://(\[[^]]+\]|[^:/?#]+):([0-9]+).*#\2#p')
if [[ -z "${eks_endpoint_port}" ]]; then
    eks_endpoint_protocol=$(printf "%s" "${eks_cluster_endpoint}" | sed -nE 's#^([^:]+)://.*#\1#p')
    if [[ "${eks_endpoint_protocol}" == "http" ]]; then
        eks_endpoint_port=80
    elif [[ "${eks_endpoint_protocol}" == "https" ]]; then
        eks_endpoint_port=443
    fi
fi

# Determine if EKS endpoint targets localhost
is_eks_endpoint_for_localhost=false
if [[ "${eks_endpoint_host}" == "localhost" || \
      "${eks_endpoint_host}" == "127.0.0.1" || \
      "${eks_endpoint_host}" == "[::1]"     || \
      "${eks_endpoint_host}" == "[0000:0000:0000:0000:0000:0000:0000:0001]" || \
      "${eks_endpoint_host}" == "[0:0000:0000:0000:0000:0000:0000:1]" || \
      "${eks_endpoint_host}" == "0.0.0.0" ]]; then
    is_eks_endpoint_for_localhost=true
fi

# Find K3s container configurations that EKS spawned through MiniStack
k3s_container_port=""
k3s_container_host_port=""
k3s_container_name=""
if [[ "${is_eks_endpoint_for_localhost}" == "true" ]]; then
    k3s_container_host_port="${eks_endpoint_port}"
    while IFS= read -r container_name; do
        container_json_configurations=$(docker inspect "${container_name}" | jq '.[0]')
        container_ports=$(printf "%s" "${container_json_configurations}"   | jq '.NetworkSettings.Ports')
        if [[ $(printf "%s" "${container_ports}" | jq 'length') -eq 0 ]]; then continue; fi
        container_tcp=$(printf "%s" "${container_ports}"       | jq --raw-output 'keys[0]')
        container_host_port=$(printf "%s" "${container_ports}" | jq --raw-output --arg tcp "${container_tcp}" '.[$tcp][0].HostPort')
        if [[ "${container_host_port}" == "${k3s_container_host_port}" ]]; then
            k3s_container_name="${container_name}"
            k3s_container_port="${container_tcp%/*}"
            break
        fi
    done < <(printf "%s" "${main_network_containers}" | jq --raw-output 'to_entries[] | .value.Name')
else
    k3s_container_port="${eks_endpoint_port}"
    while IFS= read -r container_name; do
        container_json_configurations=$(docker inspect "${container_name}" | jq '.[0]')
        container_ports=$(printf "%s" "${container_json_configurations}"   | jq '.NetworkSettings.Ports')
        if [[ $(printf "%s" "${container_ports}" | jq 'length') -eq 0 ]]; then continue; fi
        container_tcp=$(printf "%s" "${container_ports}" | jq --raw-output 'keys[0]')
        container_port="${container_tcp%/*}"
        if [[ "${container_port}" == "${k3s_container_port}" ]]; then
            k3s_container_name="${container_name}"
            k3s_container_host_port=$(printf "%s" "${container_ports}" | jq --raw-output --arg tcp "${container_tcp}" '.[$tcp][0].HostPort')
            break
        fi
    done < <(printf "%s" "${main_network_containers}" | jq --raw-output 'to_entries[] | .value.Name')
fi
if [[ -z "${k3s_container_name}" || "${k3s_container_name}" == "null" ]]; then
    echo "No K3s container with port '${k3s_container_port}' found in the network '${main_network_name}'." 1>&2
    exit 1
fi

# Check K3s container ports
if [[ -z "${k3s_container_host_port}" || "${k3s_container_host_port}" == "null" ]]; then
    echo "No Host Port found for K3s container '${k3s_container_name}'." 1>&2
    exit 1
fi
if [[ -z "${k3s_container_port}" || "${k3s_container_port}" == "null" ]]; then
    echo "No Port found for K3s container '${k3s_container_name}'." 1>&2
    exit 1
fi

# Get K3s container configurations
k3s_container_json_configurations=$(docker inspect "${k3s_container_name}"  | jq '.[0]')
k3s_container_networks=$(printf "%s" "${k3s_container_json_configurations}" | jq '.NetworkSettings.Networks')

# Get K3s container IP
k3s_container_ip=$(printf "%s" "${k3s_container_networks}" | jq --raw-output --arg network "${main_network_name}" '.[$network].IPAddress')
if [[ -z "${k3s_container_ip}" || "${k3s_container_ip}" == "null" ]]; then
    echo "No IP found for K3s container '${k3s_container_name}' in network '${main_network_name}'." 1>&2
    exit 1
fi

# Define configuration files directory path in K3s container
k3s_container_configuration_files_directory_path="/etc/rancher/k3s"

# Disable TLS verification for patched URLs that aren't in the original K3s cert SANs
docker exec "${k3s_container_name}" sh -c 'kubectl config set-cluster $(kubectl config current-context) --insecure-skip-tls-verify=true' 1>/dev/null

# Get raw kubeconfig file in K3s container
raw_kubeconfig=$(docker exec "${k3s_container_name}" cat "${k3s_container_configuration_files_directory_path}/k3s.yaml")

# Write kubeconfig for localhost in defined file
printf "%s" "${raw_kubeconfig//https:\/\/127.0.0.1:"${k3s_container_port}"/https:\/\/127.0.0.1:"${k3s_container_host_port}"}" \
    > "${kubeconfig_for_localhost_file_path}"

# Write kubeconfig for docker in defined file
printf "%s" "${raw_kubeconfig//https:\/\/127.0.0.1:"${k3s_container_port}"/https:\/\/"${k3s_container_name}":"${k3s_container_port}"}" \
    > "${kubeconfig_for_docker_file_path}"

# Copy registries.yaml into K3s container to redirect requests to ECR
docker exec "${k3s_container_name}" mkdir -p "${k3s_container_configuration_files_directory_path}" 1>/dev/null
docker cp "${k3s_registries_file_path}" "${k3s_container_name}:${k3s_container_configuration_files_directory_path}/registries.yaml" 1>/dev/null

# Restart K3s container to apply registries.yaml
docker restart "${k3s_container_name}" 1>/dev/null

# Wait until it restarts successfully
export KUBECONFIG="${kubeconfig_for_localhost_file_path}"
max_wait=300; elapsed=0; k3s_ready=false
while true; do
    sleep 5
    elapsed=$((elapsed + 5))
    if kubectl get nodes --request-timeout=5s &>/dev/null; then
        k3s_ready=true
        break
    fi
    if (( elapsed >= max_wait )); then break; fi
done

# Inform K3s status
if [[ "${k3s_ready}" == "false" ]]; then
    echo "K3s container did not recover after waiting ${max_wait}s." 1>&2
    exit 1
fi

# Wait until safe for deployment
kubectl wait --for=condition=Ready nodes --all --timeout=5m 1>/dev/null

jq --null-input --compact-output \
    --arg k3s_container_ip                   "${k3s_container_ip}" \
    --arg k3s_container_host_port            "${k3s_container_host_port}" \
    --arg kubeconfig_for_localhost_file_path "${kubeconfig_for_localhost_file_path}" \
    --arg kubeconfig_for_docker_file_path    "${kubeconfig_for_docker_file_path}" \
    '{
        k3s_container_ip:                   $k3s_container_ip,
        k3s_container_host_port:            $k3s_container_host_port,
        kubeconfig_for_localhost_file_path: $kubeconfig_for_localhost_file_path,
        kubeconfig_for_docker_file_path:    $kubeconfig_for_docker_file_path
    }'