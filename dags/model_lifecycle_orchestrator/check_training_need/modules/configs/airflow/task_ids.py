from enum import StrEnum

class TaskIDsGroup(StrEnum):
    no_action = "no_action"
    dispatch_training_approval = "dispatch_training_approval"
    setup_training_approval = "setup_training_approval"

class NoActionTaskIDs(StrEnum):
    no_drift = f"{TaskIDsGroup.no_action}.no_drift"
    no_expired_promote_pending_workflow_with_replacement = f"{TaskIDsGroup.no_action}.no_expired_promote_pending_workflow_with_replacement"
    no_expired_workflows = f"{TaskIDsGroup.no_action}.no_expired_workflows"

class DispatchTrainingApprovalTaskIDs(StrEnum):
    cold_start = f"{TaskIDsGroup.dispatch_training_approval}.cold_start"
    drifted = f"{TaskIDsGroup.dispatch_training_approval}.drifted"

class SetupTrainingApprovalTaskIDs(StrEnum):
    post = f"{TaskIDsGroup.setup_training_approval}.post"
    replace = f"{TaskIDsGroup.setup_training_approval}.replace"