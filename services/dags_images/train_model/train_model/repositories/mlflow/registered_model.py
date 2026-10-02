from imblearn.pipeline import Pipeline
from mlflow.models import infer_signature
from numpy import ndarray

from shared.modules.configs.mlflow import MLflowConfig
from shared.repositories.mlflow.mlflow import mlflow_module
from train_model.modules.schemas.mlflow import MLflowRegisteredModelInfo

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
            "imbalanced-learn==0.14.2",
            "xgboost==3.4.1",
            "scikit-learn==1.9.0",
            "numpy==2.5.2",
            "pandas==2.3.3",
        ],
        name=MLflowConfig.model_path,
        serialization_format=mlflow_module.sklearn.SERIALIZATION_FORMAT_SKOPS,
        skops_trusted_types=[
            "imblearn.over_sampling._smote.base.SMOTE",
            "imblearn.pipeline.Pipeline",
            "sklearn.metrics._dist_metrics.EuclideanDistance64",
            "sklearn.neighbors._kd_tree.KDTree",
            "xgboost.core.Booster",
            "xgboost.sklearn.XGBClassifier",
        ],
        pyfunc_predict_fn=model.predict_proba.__name__,
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