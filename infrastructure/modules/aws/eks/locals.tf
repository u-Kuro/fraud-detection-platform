locals {
  # Local Files
  # /base64
  base64_kubeconfig_for_docker_file_path = filebase64(data.external.k3s_configuration.result.kubeconfig_for_docker_file_path)
}