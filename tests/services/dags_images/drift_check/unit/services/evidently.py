from pandas import DataFrame
from pytest_mock import MockerFixture

from drift_check.modules.configs.evidently import EvidentlyConfig
from drift_check.services.evidently import extract_drift_summary, run_drift_report
from shared.modules.configs.dataset import DatasetConfig
from shared.modules.schemas.models_dataset.fraud_classification import FraudClassificationFeaturesKeys
from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences

def test_extract_drift_summary():
    feature_name = "feature"
    summary = extract_drift_summary(
        results={
            "metrics": [
                {
                    "metric": "DataDriftPreset",
                    "result": {
                        "drift_by_columns": {
                            feature_name: { "drift_detected": True },
                        },
                        "share_drifted_features": 1.0,
                        "number_of_drifted_features": 1,
                        "number_of_columns": 1,
                        "dataset_drift": True,
                    }
                },
                {
                    "metric": "ClassificationQualityMetric",
                    "result": {
                        "current": { "f1": 1.0 },
                        "reference": { "f1": 0.0 },
                    }
                }
            ]
        },
        feature_names={ feature_name }
    )

    assert EvidentlyConfig.data_drift_key in summary
    assert EvidentlyConfig.concept_drift_key in summary

    data_drift = summary[EvidentlyConfig.data_drift_key]
    assert EvidentlyConfig.drifted_key in data_drift

    concept_drift = summary[EvidentlyConfig.concept_drift_key]
    assert EvidentlyConfig.drifted_key in concept_drift

def test_run_drift_report(mocker: MockerFixture):
    number_of_class = 2
    minimum_sample_per_class = 1
    minimum_sample = number_of_class * minimum_sample_per_class
    dataframe = DataFrame({
        TransactionInferences.is_fraud.key: [1] * minimum_sample_per_class + [0] * minimum_sample_per_class,
        TransactionInferences.is_fraud_prediction.key: [1] * minimum_sample_per_class + [0] * minimum_sample_per_class,
        TransactionInferences.amount.key: [1.0] * minimum_sample,
        TransactionInferences.transaction_timestamp.key: [1] * minimum_sample,
        **{key: [1.0] * minimum_sample for key in FraudClassificationFeaturesKeys},
    })

    mocker.patch.object(
        target=DatasetConfig,
        attribute="minimum_rows",
        new=len(dataframe.index)
    )

    summary, html_bytes = run_drift_report(dataframe, dataframe)

    assert isinstance(summary, dict)
    assert isinstance(html_bytes, bytes)