resource "docker_image" "fraud_detection_platform_act" {
  name = "fraud_detection_platform_act:latest"

  build {
    context    = path.cwd
    dockerfile = ".github/Dockerfile"
  }
}