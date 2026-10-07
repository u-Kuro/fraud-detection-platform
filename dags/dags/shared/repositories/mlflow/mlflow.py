from functools import cache
from os import environ

import mlflow
from mlflow import MlflowClient, MlflowException

from dags.shared.modules.utilities.retry import retry
from dags.shared.modules.configs.mlflow import MLflowConfig

@cache
def initialize_mlflow() -> None:
    # Workaround: without this, downloading the reference dataset from MLflow fails (cause unknown)
    environ["MLFLOW_ENABLE_PROXY_MULTIPART_DOWNLOAD"] = "false"
    # Sets prefixed Apache Airflow environment to its official environment name
    environ["MLFLOW_TRACKING_USERNAME"] = MLflowConfig.MLFLOW_TRACKING_USERNAME()
    environ["MLFLOW_TRACKING_PASSWORD"] = MLflowConfig.MLFLOW_TRACKING_PASSWORD()

    mlflow.set_tracking_uri(MLflowConfig.MLFLOW_TRACKING_URI())
    mlflow.set_workspace(MLflowConfig.MLFLOW_WORKSPACE())

    # warmup tracking
    # for attempt in retry(ignored_exceptions=MlflowException):
    #     with attempt:
    #         mlflow.set_experiment(experiment_name)
    # warmup registry
    for attempt in retry(ignored_exceptions=MlflowException):
        with attempt:
            mlflow.search_registered_models(max_results=1)

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