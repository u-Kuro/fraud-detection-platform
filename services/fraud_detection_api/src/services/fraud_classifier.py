import pandas

from fraud_detection_api.src.modules.configs.fraud_classifier import FraudClassifierConfig
from fraud_detection_api.src.modules.schemas.inferences.fraud_classification import FraudClassificationRequest, FraudClassificationOutput
from fraud_detection_api.src.repositories.mlflow.models import MlflowModel
from services_shared.src.modules.schemas.models_dataset.fraud_classification import FraudClassificationFeaturesKeys

class FraudClassifier(MlflowModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def classify(
        self,
        transaction_details: FraudClassificationRequest
    ) -> FraudClassificationOutput:
        features = transaction_details.model_dump(
            include=set(FraudClassificationFeaturesKeys)
        )

        features_df = pandas.DataFrame([features])
        features_df[FraudClassificationFeaturesKeys.transaction_timestamp] = features_df[
            FraudClassificationFeaturesKeys.transaction_timestamp
        ].apply(lambda x: int(x.timestamp()))

        fraud_probability = float(self.model.predict(features_df.values)[0][1])
        fraud_prediction = fraud_probability > FraudClassifierConfig.classification_threshold

        return FraudClassificationOutput(
            **self.deployed_model.model_dump(),
            **transaction_details.model_dump(),
            is_fraud=None,
            is_fraud_probability=fraud_probability,
            is_fraud_prediction=fraud_prediction,
        )