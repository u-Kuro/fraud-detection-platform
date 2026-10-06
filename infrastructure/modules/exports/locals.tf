locals {
  # EKS
  # /resource-names
  eks_k8s_base_config_map_name        = "base"
  eks_k8s_base_secret_name            = "base"
  eks_k8s_docker_registry_secret_name = "docker-registry"

  # MWAA
  # /connections
  mwaa_connections_k8s_connection_id      = "k8s"
  mwaa_connections_postgres_connection_id = "postgres"
  mwaa_connections_s3_connection_id       = "s3"
  # /variables (Prefixed with AIRFLOW_VAR_ so Fixed won't work)
  mwaa_variables_k8s_base_config_map_name        = "K8S_BASE_CONFIG_MAP_NAME"
  mwaa_variables_k8s_base_secret_name            = "K8S_BASE_SECRET_NAME"
  mwaa_variables_k8s_connection_id_name          = "K8S_CONNECTION_ID"
  mwaa_variables_k8s_docker_registry_secret_name = "K8S_DOCKER_REGISTRY_SECRET_NAME"
  mwaa_variables_k8s_namespace                   = "K8S_NAMESPACE"

  mwaa_variables_mlflow_tracking_uri      = "MLFLOW_TRACKING_URI"
  mwaa_variables_mlflow_tracking_username = "MLFLOW_TRACKING_USERNAME"
  mwaa_variables_mlflow_tracking_password = "MLFLOW_TRACKING_PASSWORD"
  mwaa_variables_mlflow_workspace         = "MLFLOW_WORKSPACE"

  mwaa_variables_postgres_connection_id_name = "POSTGRES_CONNECTION_ID"

  mwaa_variables_s3_connection_id_name = "S3_CONNECTION_ID"
  mwaa_variables_s3_bucket             = "S3_BUCKET"

  mwaa_variables_environment_name = "MWAA_ENVIRONMENT_NAME"
  mwaa_variables_environment_url  = "AWS_ENDPOINT_URL_MWAA"
}