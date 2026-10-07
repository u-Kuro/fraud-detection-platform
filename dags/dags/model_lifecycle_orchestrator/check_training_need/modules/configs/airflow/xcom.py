from enum import StrEnum

class DriftCheckXComKeys(StrEnum):
    has_enough_current_data = "has_enough_current_data"
    drift_detected = "drift_detected"
    drift_summary = "drift_summary"