from pandas import DataFrame
from sklearn.preprocessing import RobustScaler
from xgboost import XGBClassifier

from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences
from train_model.modules.configs.hyperparameters import XGBHyperparametersSampler
from train_model.services.preprocessing import preprocess
from train_model.services.training import train_model

def test_train_model():
    number_of_class = 2
    minimum_sample_per_class = 5
    dataframe = preprocess(
        dataset=DataFrame({
            "feature": [1] * number_of_class * minimum_sample_per_class,
            TransactionInferences.is_fraud.key: [0] * minimum_sample_per_class + [1] * minimum_sample_per_class
        })
    )

    train_model(
        preprocess_outputs=dataframe,
        scaler=RobustScaler,
        model=XGBClassifier,
        hyperparameters_sampler=XGBHyperparametersSampler
    )