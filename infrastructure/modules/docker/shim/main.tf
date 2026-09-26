resource "docker_image" "fraud_detection_platform_shim" {
  name = "fraud_detection_platform_shim:latest"

  build {
    context    = path.cwd
    dockerfile = "infrastructure/modules/docker/shim/fraud_detection_platform_shim/Dockerfile"
  }
}

resource "docker_container" "fraud_detection_platform_shim" {
  name  = var.shim_container_name
  image = docker_image.fraud_detection_platform_shim.image_id

  network_mode = var.main_network_name
  networks_advanced {
    name    = var.main_network_name
    aliases = ["api.github.com.shim"]
  }

  volumes {
    from_container = var.RUNNER_CONTAINER_NAME
  }

  user = var.HOST_USER != "" ? var.HOST_USER : null
  env = concat(
    [
      "RUNNER_CONTAINER_NAME=${var.shim_container_name}",
      "ACT_IMAGE=${var.act_image_name}",
    ],
    var.HOST_USER != "" ? ["HOST_USER=${var.HOST_USER}"] : []
  )
}