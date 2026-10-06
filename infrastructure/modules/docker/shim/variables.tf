# Act
# /configurations
variable "act_image_name" { type = string }

# Docker
# /configurations
variable "main_network_name" { type = string }

# IAM
# /admin
variable "iam_admin_access_key" {
  type = string
  sensitive = true
}
variable "iam_admin_secret_key" {
  type = string
  sensitive = true
}
variable "iam_admin_region" { type = string }

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