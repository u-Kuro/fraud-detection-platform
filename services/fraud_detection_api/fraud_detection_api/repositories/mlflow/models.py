from mlflow.pyfunc import PyFuncModel

from fraud_detection_api.modules.schemas.mlflow import DeployedModel
from shared.repositories.mlflow.mlflow import mlflow_module

class MlflowModel:
    def __init__(self, deployed_model: DeployedModel):
        self.deployed_model = deployed_model
        self.model: PyFuncModel = mlflow_module.pyfunc.load_model(
            model_uri=f"models:/{deployed_model.model_name}/{deployed_model.model_version}"
        )