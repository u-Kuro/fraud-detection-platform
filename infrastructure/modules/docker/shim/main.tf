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

  networks_advanced {
    name = var.main_network_name
    aliases = [
      "api.github.com.shim"
    ]
  }

  volumes {
    from_container = var.RUNNER_CONTAINER_NAME
  }

  user = var.HOST_USER != "" ? var.HOST_USER : null
  env = concat(
    [
      # Docker
      "ACT_IMAGE=${var.act_image_name}",
      "RUNNER_CONTAINER_NAME=${var.shim_container_name}",
      # MWAA
      "AWS_ACCESS_KEY_ID=${var.iam_admin_access_key}",
      "AWS_DEFAULT_REGION=${var.iam_admin_region}",
      "AWS_SECRET_ACCESS_KEY=${var.iam_admin_secret_key}",
    ],
    var.HOST_USER != "" ? ["HOST_USER=${var.HOST_USER}"] : []
  )
}