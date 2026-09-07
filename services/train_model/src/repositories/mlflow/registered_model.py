from mlflow.models import infer_signature
from numpy import ndarray
from sklearn.pipeline import Pipeline

from services.shared.src.modules.configs.mlflow import MLflowConfig
from services.shared.src.repositories.mlflow.mlflow import mlflow_module
from services.train_model.src.modules.schemas.mlflow import MLflowRegisteredModelInfo

def save_and_register_model(
    model: Pipeline,
    x_test_samples: ndarray,
) -> MLflowRegisteredModelInfo:
    model_info = mlflow_module.sklearn.log_model(
        sk_model=model,
        registered_model_name=MLflowConfig.model_name,
        signature=infer_signature(
            model_input=x_test_samples,
            model_output=model.predict(x_test_samples)
        ),
        input_example=x_test_samples,
        pip_requirements=[
            "xgboost==3.4.1",
            "scikit-learn==1.9.0",
            "numpy==2.5.2",
            "pandas==2.3.3",
        ],
        name=MLflowConfig.model_path,
        pyfunc_predict_fn=model.predict_proba.__name__
    )

    if isinstance(model_info.registered_model_version, int):
        return MLflowRegisteredModelInfo(
            run_id=model_info.run_id,
            model_id=model_info.model_id,
            model_name=MLflowConfig.model_name,
            model_version=model_info.registered_model_version
        )
    else:
        raise RuntimeError("Model registration failed: registered_model_version is not an integer.")