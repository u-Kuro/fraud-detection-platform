from os import environ

import mlflow
from mlflow import MlflowClient

from dags.shared.modules.configs.mlflow import MLflowConfig

def initialize_mlflow():
    # Sets prefixed Apache Airflow environment to its official environment name
    environ["MLFLOW_TRACKING_USERNAME"] = MLflowConfig.mlflow_tracking_username()
    environ["MLFLOW_TRACKING_PASSWORD"] = MLflowConfig.mlflow_tracking_password()

    mlflow.set_tracking_uri(MLflowConfig.mlflow_tracking_uri())
    mlflow.set_workspace(MLflowConfig.mlflow_workspace())

def get_mlflow_client() -> MlflowClient:
    initialize_mlflow()
    return MlflowClient(
        tracking_uri=MLflowConfig.mlflow_tracking_uri()
    )

def get_mlflow():
    initialize_mlflow()
    return mlflow

mlflow_client: MlflowClient = get_mlflow_client()
mlflow_module = get_mlflow()