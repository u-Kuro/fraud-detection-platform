from os import environ

import mlflow
from mlflow import MlflowClient

from dags.shared.modules.configs.mlflow import MLflowConfig

def initialize_mlflow():
    # Sets prefixed Apache Airflow environment to its official environment name
    environ["MLFLOW_TRACKING_USERNAME"] = MLflowConfig.MLFLOW_TRACKING_USERNAME()
    environ["MLFLOW_TRACKING_PASSWORD"] = MLflowConfig.MLFLOW_TRACKING_PASSWORD()

    mlflow.set_tracking_uri(MLflowConfig.MLFLOW_TRACKING_URI())
    mlflow.set_workspace(MLflowConfig.MLFLOW_WORKSPACE())

def get_mlflow_client() -> MlflowClient:
    initialize_mlflow()
    return MlflowClient(
        tracking_uri=MLflowConfig.MLFLOW_TRACKING_URI()
    )

def get_mlflow():
    initialize_mlflow()
    return mlflow

mlflow_client: MlflowClient = get_mlflow_client()
mlflow_module = get_mlflow()