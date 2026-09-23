from drift_check.modules.configs.airflow.xcom import DriftCheckXComKeys
from drift_check.services.evidently import drift_check
from shared.controllers.airflow.xcom import xcom_push

def main() -> None:
    drift_detected, drift_summary = drift_check()
    xcom_push({
        DriftCheckXComKeys.drift_detected: drift_detected,
        DriftCheckXComKeys.drift_summary: drift_summary
    })

if __name__ == "__main__":
    main()