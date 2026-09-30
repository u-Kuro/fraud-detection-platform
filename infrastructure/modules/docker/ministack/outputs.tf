# MiniStack
# /configurations
output "name" { value = docker_container.ministack.name }
output "port" { value = local.ministack_container_port }
output "host_port" { value = local.ministack_container_host_port }
output "ip" { value = local.ministack_container_ip }
# /urls
output "endpoint" { value = "${docker_container.ministack.name}:${local.ministack_container_port}" }
output "url" { value = "http://${docker_container.ministack.name}:${local.ministack_container_port}" }
output "egress_url" { value = "http://${local.ministack_container_ip}:${local.ministack_container_port}" }
output "host_url" { value = "http://localhost:${local.ministack_container_host_port}" }
output "host_docker_internal_url" { value = "http://host.docker.internal:${local.ministack_container_host_port}" }