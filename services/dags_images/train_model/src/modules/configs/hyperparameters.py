from dataclasses import dataclass, fields
from typing import Callable

from optuna import Trial

@dataclass(frozen=True)
class XGBHyperparametersSampler:
    type HyperparameterSampler = Callable[[Trial], int | float]

    n_estimators: HyperparameterSampler = lambda trial: trial.suggest_int("n_estimators", 100, 500)
    max_depth: HyperparameterSampler = lambda trial: trial.suggest_int("max_depth", 3, 10)
    learning_rate: HyperparameterSampler = lambda trial: trial.suggest_float("learning_rate", 0.005, 0.3, log=True)
    subsample: HyperparameterSampler = lambda trial: trial.suggest_float("subsample", 0.5, 1.0)
    colsample_bytree: HyperparameterSampler = lambda trial: trial.suggest_float("colsample_bytree", 0.4, 1.0)
    reg_alpha: HyperparameterSampler = lambda trial: trial.suggest_float("reg_alpha", 1e-6, 1.0, log=True)
    reg_lambda: HyperparameterSampler = lambda trial: trial.suggest_float("reg_lambda", 1e-6, 5.0, log=True)
    gamma: HyperparameterSampler = lambda trial: trial.suggest_float("gamma", 0.0, 5.0)
    min_child_weight: HyperparameterSampler = lambda trial: trial.suggest_int("min_child_weight", 1, 10)

    def resolve(self, trial: Trial) -> dict[str, int | float]:
        return {
            field.name: getattr(self, field.name)(trial)
            for field in fields(self)
        }