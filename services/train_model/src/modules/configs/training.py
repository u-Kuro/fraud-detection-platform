from dataclasses import dataclass

@dataclass(frozen=True)
class TrainingConfig:
    random_state: int = 42
    test_size: float = 0.2
    bayes_steps: int = 30
    training_timeout_seconds: int = 3_600
    cv_val_size: float = test_size / (1 - test_size)