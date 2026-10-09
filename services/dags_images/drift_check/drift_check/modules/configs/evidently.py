from dataclasses import dataclass

@dataclass(frozen=True)
class EvidentlyConfig:
    data_drift_key: str = "data_drift"
    concept_drift_key: str = "concept_drift"
    drifted_key: str = "drifted"

    minimum_fraud_samples: int = 100
    share_of_drifted_features_threshold: float = 0.5
    average_precision_delta_threshold: float = -0.1