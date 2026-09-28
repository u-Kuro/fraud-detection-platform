from enum import StrEnum

class DAGIDs(StrEnum):
    check_training_need = "check_training_need"
    cold_start = "cold_start"
    on_promotion_decision = "on_promotion_decision"
    on_training_decision = "on_training_decision"