# Create main network for infrastructure
resource "docker_network" "main" {
  name = "fraud-detection-platform-network"
  ipam_config {
    subnet  = var.main_docker_network_subnet
    gateway = cidrhost(var.main_docker_network_subnet, 1) # 10.232.0.1
  }
}
# Clean-up all containers of main network before deleting
resource "terraform_data" "force_delete_network" {
  input = docker_network.main.name
  provisioner "local-exec" {
    when        = destroy
    interpreter = ["pwsh", "-File"]
    command     = "${path.module}/scripts/remove-main-network-containers.ps1"
    environment = {
      MAIN_NETWORK_NAME = self.output
    }
  }
}