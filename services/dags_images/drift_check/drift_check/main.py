from drift_check.modules.configs.airflow.xcom import DriftCheckXComKeys
from drift_check.services.evidently import drift_check
from drift_check.repositories.mlflow.registered_model_dataset import load_reference_dataset
from drift_check.repositories.postgres.transaction_inferences import load_current_dataset
from shared.controllers.airflow.xcom import xcom_push
from shared.modules.configs.dataset import DatasetConfig

def main() -> None:
    df_reference, current_dataset_cutoff = load_reference_dataset()
    df_current = load_current_dataset(current_dataset_cutoff)

    if len(df_current) < DatasetConfig.minimum_rows:
        xcom_push({
            DriftCheckXComKeys.has_enough_current_data: False
        })
    else:
        drift_detected, drift_summary = drift_check(df_reference, df_current)

        xcom_push({
            DriftCheckXComKeys.has_enough_current_data: True,
            DriftCheckXComKeys.drift_detected: drift_detected,
            DriftCheckXComKeys.drift_summary: drift_summary
        })

if __name__ == "__main__":
    main()