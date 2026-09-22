import numpy
import pandas
from pandas import DataFrame

from train_model.src.modules.schemas.postgres.model_deployment_workflows import ModelDeploymentWorkflowDatasetTimestamps

def get_dataset_min_and_max_timestamps(
    dataset: DataFrame,
    timestamp_feature_key: str
) -> ModelDeploymentWorkflowDatasetTimestamps:
    transaction_timestamps = dataset[timestamp_feature_key]

    min_timestamp = transaction_timestamps.min()
    max_timestamp = transaction_timestamps.max()

    assert isinstance(min_timestamp, numpy.integer)
    assert isinstance(max_timestamp, numpy.integer)

    min_timestamp = pandas.Timestamp(min_timestamp, unit="s", tz="UTC")
    max_timestamp = pandas.Timestamp(max_timestamp, unit="s", tz="UTC")

    assert isinstance(min_timestamp, pandas.Timestamp)
    assert isinstance(max_timestamp, pandas.Timestamp)

    return ModelDeploymentWorkflowDatasetTimestamps(
        model_dataset_min_iso_datetime=min_timestamp.isoformat(),
        model_dataset_max_iso_datetime=max_timestamp.isoformat(),
    )