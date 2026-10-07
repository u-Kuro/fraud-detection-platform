from functools import cache

import mlflow
from mlflow import MlflowClient, MlflowException

from shared.modules.utilities.retry import retry
from shared.modules.configs.mlflow import MLflowConfig
from shared.modules.environment.mlflow import mlflow_environment

@cache
def initialize_mlflow() -> None:
    mlflow.set_tracking_uri(mlflow_environment.MLFLOW_TRACKING_URI)
    mlflow.set_workspace(mlflow_environment.MLFLOW_WORKSPACE)

    # warmup tracking
    for attempt in retry(ignored_exceptions=MlflowException):
        with attempt:
            mlflow.set_experiment(MLflowConfig.experiment_name)

    # warmup registry
    for attempt in retry(ignored_exceptions=MlflowException):
        with attempt:
            mlflow.search_registered_models(max_results=1)

def get_mlflow_client() -> MlflowClient:
    initialize_mlflow()
    return MlflowClient()

def get_mlflow():
    initialize_mlflow()
    return mlflow

mlflow_client: MlflowClient = get_mlflow_client()
mlflow_module = get_mlflow()