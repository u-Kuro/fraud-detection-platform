import time
from functools import cache

import mlflow
from mlflow import MlflowClient, MlflowException

from shared.modules.configs.mlflow import MLflowConfig
from shared.modules.environment.mlflow import mlflow_environment

@cache
def initialize_mlflow() -> None:
    mlflow.set_tracking_uri(mlflow_environment.MLFLOW_TRACKING_URI)
    mlflow.set_workspace(mlflow_environment.MLFLOW_WORKSPACE)
    attempts = 5
    for attempt in range(1, attempts + 1):
        try:
            mlflow.set_experiment(MLflowConfig.experiment_name)
            break
        except MlflowException:
            if attempt == attempts: raise
            time.sleep(5)

def get_mlflow_client() -> MlflowClient:
    initialize_mlflow()
    return MlflowClient()

def get_mlflow():
    initialize_mlflow()
    return mlflow

mlflow_client: MlflowClient = get_mlflow_client()
mlflow_module = get_mlflow()