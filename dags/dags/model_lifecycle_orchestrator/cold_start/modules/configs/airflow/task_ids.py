from enum import StrEnum

class TaskIDsGroup(StrEnum):
    no_action = "no_action"

class NoActionTaskIDs(StrEnum):
    has_transaction_inferences = f"{TaskIDsGroup.no_action}-has_transaction_inferences"