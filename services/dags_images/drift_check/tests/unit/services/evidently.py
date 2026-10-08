import json
from enum import Enum

from pandas import DataFrame
from pytest import approx
from pytest_mock import MockerFixture

from drift_check.modules.configs.evidently import EvidentlyConfig
from drift_check.services.evidently import (
    drift_check,
    get_drifted_columns,
    get_metrics,
    run_drift_report,
    summarize_concept_drift,
    summarize_data_drift,
)
from shared.modules.schemas.models_dataset.fraud_classification import FraudClassificationFeaturesKeys
from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences

def test_get_metrics():
    dataframe = DataFrame({
        TransactionInferences.is_fraud.key:            [1, 1, 0, 0, 0, 0],
        TransactionInferences.is_fraud_prediction.key: [1, 0, 1, 1, 0, 0],
    })

    precision, recall, f1 = get_metrics(dataframe)

    assert precision == approx(1 / 3)
    assert recall == approx(1 / 2)
    assert f1 == approx(2 / 5)

def test_get_drifted_columns():
    class Status(Enum):
        FAIL = "FAIL"

    def make_result(test_type: str, column: str, status) -> dict:
        return {
            "status": status,
            "metric_config": {"params": {"type": test_type, "column": column}},
        }

    results = {
        "tests": [
            make_result("evidently:metric_v2:ValueDrift", "drifted_feature", "FAIL"),
            make_result("evidently:metric_v2:ValueDrift", "drifted_feature_enum_status", Status.FAIL),
            make_result("evidently:metric_v2:ValueDrift", "stable_feature", "SUCCESS"),
            make_result("evidently:metric_v2:F1Score", "not_a_drift_test", "FAIL"),
        ]
    }

    assert get_drifted_columns(results) == {"drifted_feature", "drifted_feature_enum_status"}

def test_summarize_data_drift():
    features = ["feature_a", "feature_b"]

    all_features_drifted = summarize_data_drift(
        drifted_columns=set(features),
        features=features
    )
    assert all_features_drifted == {
        "number_of_features": 2,
        "number_of_drifted_features": 2,
        "share_of_drifted_features": 1.0,
        EvidentlyConfig.drifted_key: True,
    }

    nothing_drifted = summarize_data_drift(
        drifted_columns=set(),
        features=features
    )
    assert nothing_drifted["number_of_drifted_features"] == 0
    assert nothing_drifted[EvidentlyConfig.drifted_key] is False

    only_score_drifted = summarize_data_drift(
        drifted_columns={TransactionInferences.is_fraud_probability.key},
        features=features,
    )
    assert only_score_drifted["number_of_drifted_features"] == 0
    assert only_score_drifted[EvidentlyConfig.drifted_key] is True

def test_summarize_concept_drift():
    labels = [1, 1, 0, 0]
    perfect = DataFrame({
        TransactionInferences.is_fraud.key: labels,
        TransactionInferences.is_fraud_prediction.key: labels,
    })
    inverted = DataFrame({
        TransactionInferences.is_fraud.key: labels,
        TransactionInferences.is_fraud_prediction.key: [0, 0, 1, 1],
    })

    skipped = summarize_concept_drift(
        df_current=inverted,
        df_reference=perfect,
        has_sufficient_fraud_samples=False,
    )
    assert skipped == {EvidentlyConfig.drifted_key: False}

    degraded = summarize_concept_drift(
        df_current=inverted,
        df_reference=perfect,
        has_sufficient_fraud_samples=True,
    )
    assert degraded["f1"] == approx(0.0)
    assert degraded["precision_delta"] == approx(-1.0)
    assert degraded["recall_delta"] == approx(-1.0)
    assert degraded["f1_delta"] == approx(-1.0)
    assert degraded[EvidentlyConfig.drifted_key] is True

    stable = summarize_concept_drift(
        df_current=perfect,
        df_reference=perfect,
        has_sufficient_fraud_samples=True,
    )
    assert stable["f1_delta"] == approx(0.0)
    assert stable[EvidentlyConfig.drifted_key] is False

def test_run_drift_report():
    samples_per_class = EvidentlyConfig.minimum_fraud_samples
    number_of_samples = 2 * samples_per_class
    labels = [1] * samples_per_class + [0] * samples_per_class
    dataframe = DataFrame({
        TransactionInferences.is_fraud.key: labels,
        TransactionInferences.is_fraud_prediction.key: labels,
        TransactionInferences.is_fraud_probability.key: [float(label) for label in labels],
        TransactionInferences.amount.key: [1.0] * number_of_samples,
        TransactionInferences.transaction_timestamp.key: [1] * number_of_samples,
        **{key: [1.0] * number_of_samples for key in FraudClassificationFeaturesKeys},
    })

    summary, html_bytes = run_drift_report(dataframe, dataframe)

    assert set(summary) == {EvidentlyConfig.data_drift_key, EvidentlyConfig.concept_drift_key}
    assert summary[EvidentlyConfig.data_drift_key][EvidentlyConfig.drifted_key] is False
    assert summary[EvidentlyConfig.concept_drift_key][EvidentlyConfig.drifted_key] is False
    assert "f1" in summary[EvidentlyConfig.concept_drift_key]
    assert isinstance(html_bytes, bytes)
    assert len(html_bytes) > 0

def test_drift_check(mocker: MockerFixture):
    html_bytes = b"<html></html>"
    drifted_summary = {
        EvidentlyConfig.data_drift_key: {EvidentlyConfig.drifted_key: False},
        EvidentlyConfig.concept_drift_key: {EvidentlyConfig.drifted_key: True},
    }
    stable_summary = {
        EvidentlyConfig.data_drift_key: {EvidentlyConfig.drifted_key: False},
        EvidentlyConfig.concept_drift_key: {EvidentlyConfig.drifted_key: False},
    }
    run_report = mocker.patch(
        "drift_check.services.evidently.run_drift_report",
        return_value=(drifted_summary, html_bytes),
    )
    upload = mocker.patch("drift_check.repositories.s3.drift_reports.upload_drift_report")

    drift_detected, summary = drift_check(DataFrame(), DataFrame())

    assert drift_detected is True
    assert summary == drifted_summary
    upload.assert_called_once_with(html_bytes, json.dumps(drifted_summary).encode())

    run_report.return_value = (stable_summary, html_bytes)

    drift_detected, summary = drift_check(DataFrame(), DataFrame())

    assert drift_detected is False
    assert summary == stable_summary