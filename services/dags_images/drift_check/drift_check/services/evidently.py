import json

from evidently import BinaryClassification, DataDefinition, Dataset, Report
from evidently.metrics import F1Score, Precision, Recall, ValueDrift
from evidently.presets import DataDriftPreset
from pandas import DataFrame
from sklearn.metrics import f1_score, precision_score, recall_score

from drift_check.modules.configs.evidently import EvidentlyConfig
from drift_check.repositories.s3.drift_reports import upload_drift_report
from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences

def get_metrics(df: DataFrame) -> tuple[float, float, float]:
    y_true = df[TransactionInferences.is_fraud.key].astype(int)
    y_pred = df[TransactionInferences.is_fraud_prediction.key].astype(int)
    return (
        float(precision_score(y_true, y_pred, zero_division=0)),
        float(recall_score(y_true, y_pred, zero_division=0)),
        float(f1_score(y_true, y_pred, zero_division=0)),
    )

def get_drifted_columns(results: dict) -> set[str]:
    drifted_columns: set[str] = set()
    for test in results["tests"]:
        status = test["status"]
        parameters = test["metric_config"]["params"]
        if parameters["type"].endswith(":ValueDrift") and getattr(status, "value", status) == "FAIL":
            drifted_columns.add(parameters["column"])

    return drifted_columns

def summarize_data_drift(
    drifted_columns: set[str],
    features: list[str],
) -> dict:
    return {
        "number_of_features": (number_of_features := len(features)),
        "number_of_drifted_features": (number_of_drifted_features := len(drifted_columns & set(features))),
        "share_of_drifted_features": (share_of_drifted_features := number_of_drifted_features / number_of_features),
        EvidentlyConfig.drifted_key: (
            share_of_drifted_features >= EvidentlyConfig.share_of_drifted_features_threshold
            or TransactionInferences.is_fraud_probability.key in drifted_columns
        ),
    }

def summarize_concept_drift(
    df_current: DataFrame,
    df_reference: DataFrame,
    has_sufficient_fraud_samples: bool,
) -> dict:
    if has_sufficient_fraud_samples:
        current_precision, current_recall, current_f1 = get_metrics(df_current)
        reference_precision, reference_recall, reference_f1 = get_metrics(df_reference)

        return {
            "precision": current_precision,
            "recall": current_recall,
            "f1": current_f1,
            "precision_delta": current_precision - reference_precision,
            "recall_delta": current_recall - reference_recall,
            "f1_delta": (f1_delta := current_f1 - reference_f1),
            EvidentlyConfig.drifted_key: f1_delta <= EvidentlyConfig.f1_delta_threshold,
        }
    else:
        return {
            "skipped": True,
            EvidentlyConfig.drifted_key: False,
        }

def run_drift_report(
    df_reference: DataFrame,
    df_current: DataFrame,
) -> tuple[dict[str, dict], bytes]:
    target_key = TransactionInferences.is_fraud.key
    prediction_key = TransactionInferences.is_fraud_prediction.key
    probability_key = TransactionInferences.is_fraud_probability.key

    non_feature_columns = {
        target_key,
        prediction_key,
        probability_key
    }
    feature_columns = sorted((set(df_current.columns) & set(df_reference.columns)) - non_feature_columns)

    number_of_fraud_samples = {
        "current": int(df_current[target_key].sum()),
        "reference": int(df_reference[target_key].sum()),
    }
    has_sufficient_fraud_samples = min(*number_of_fraud_samples.values()) >= EvidentlyConfig.minimum_fraud_samples

    report = Report(
        metrics=[
            DataDriftPreset(
                columns=feature_columns,
                drift_share=EvidentlyConfig.share_of_drifted_features_threshold,
                num_method="psi"
            ),
            ValueDrift(column=probability_key),
            *([Precision(), Recall(), F1Score()] if has_sufficient_fraud_samples else []),
        ],
        include_tests=True
    )

    data_definition = DataDefinition(
        classification=[
            BinaryClassification(
                target=target_key,
                prediction_labels=prediction_key
            )
        ],
        numerical_columns=[*feature_columns, probability_key],
    )
    result = report.run(
        current_data=Dataset.from_pandas(
            data=df_current,
            data_definition=data_definition
        ),
        reference_data=Dataset.from_pandas(
            data=df_reference,
            data_definition=data_definition
        ),
    )

    summary = {
        EvidentlyConfig.data_drift_key: summarize_data_drift(
            drifted_columns=get_drifted_columns(result.dict()),
            features=feature_columns,
        ),
        EvidentlyConfig.concept_drift_key: summarize_concept_drift(
            df_current=df_current,
            df_reference=df_reference,
            has_sufficient_fraud_samples=has_sufficient_fraud_samples
        ),
    }
    return summary, result.get_html_str(as_iframe=False).encode("utf-8")

def drift_check(df_reference: DataFrame, df_current: DataFrame) -> tuple[bool, dict[str, dict]]:
    drift_summary, html_bytes = run_drift_report(df_reference, df_current)
    upload_drift_report(html_bytes, json.dumps(drift_summary).encode())

    data_drift = drift_summary[EvidentlyConfig.data_drift_key].get(EvidentlyConfig.drifted_key, False)
    concept_drift = drift_summary[EvidentlyConfig.concept_drift_key].get(EvidentlyConfig.drifted_key, False)

    drift_detected = data_drift or concept_drift

    return drift_detected, drift_summary