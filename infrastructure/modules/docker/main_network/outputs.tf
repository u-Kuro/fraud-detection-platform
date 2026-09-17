# Docker Network
# /configurations
output "name" { value = docker_network.main.name }
output "subnet" { value = tolist(docker_network.main.ipam_config)[0].subnet }
output "gateway" { value = tolist(docker_network.main.ipam_config)[0].gateway }