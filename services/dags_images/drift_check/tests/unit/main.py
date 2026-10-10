import json
from datetime import datetime, timezone

import pytest
from pandas import DataFrame
from pytest_mock import MockerFixture

from drift_check.modules.configs.airflow.xcom import DriftCheckXComKeys
from drift_check.modules.configs.evidently import EvidentlyConfig
from shared.modules.configs.airflow import AirflowConfig
from shared.modules.configs.dataset import DatasetConfig

@pytest.mark.usefixtures("fs")
def test_main(mocker: MockerFixture):
    mocker.patch(
        "drift_check.main.load_reference_dataset",
        return_value=(DataFrame(), datetime.now(tz=timezone.utc)),
    )
    mocker.patch(
        "drift_check.main.load_current_dataset",
        return_value=DataFrame(index=range(DatasetConfig.minimum_rows)),
    )
    mocker.patch(
        target="drift_check.main.drift_check",
        return_value=(
            True,
            {
                EvidentlyConfig.data_drift_key: {},
                EvidentlyConfig.concept_drift_key: {}
            }
        ),
    )

    from drift_check.main import main
    main()

    with open(AirflowConfig.xcom_file_path) as file:
        result = json.loads(file.read())

    assert DriftCheckXComKeys.drift_detected in result
    assert DriftCheckXComKeys.drift_summary in result

    drift_detected = result[DriftCheckXComKeys.drift_detected]
    assert isinstance(drift_detected, bool)

    drift_summary = result[DriftCheckXComKeys.drift_summary]
    assert isinstance(drift_summary, dict)
    assert EvidentlyConfig.data_drift_key in drift_summary
    assert EvidentlyConfig.concept_drift_key in drift_summary