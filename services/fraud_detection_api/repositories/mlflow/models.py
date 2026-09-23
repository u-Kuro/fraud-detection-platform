import mlflow
from mlflow.pyfunc import PyFuncModel

from fraud_detection_api.modules.schemas.mlflow import DeployedModel

class MlflowModel:
    def __init__(self, deployed_model: DeployedModel):
        self.deployed_model = deployed_model
        self.model: PyFuncModel = mlflow.pyfunc.load_model(
            model_uri=f"models:/{deployed_model.model_name}/{deployed_model.model_version}"
        )