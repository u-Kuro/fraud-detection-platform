# Act
# /configurations
variable "act_image_name" { type = string }

# Docker
# /configurations
variable "main_network_name" { type = string }

# MiniStack
# /configurations
variable "shim_container_name" {
  type    = string
  default = "fraud_detection_platform_shim"
}

# Runner
# /configurations
variable "RUNNER_CONTAINER_NAME" { type = string }
variable "HOST_USER" { type = string }