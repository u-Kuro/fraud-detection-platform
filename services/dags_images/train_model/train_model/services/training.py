from typing import cast

import numpy
import optuna
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from optuna import Study
from optuna.samplers import TPESampler
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import RobustScaler
from xgboost import XGBClassifier

from shared.modules.configs.mlflow import MLflowConfig
from train_model.modules.configs.hyperparameters import XGBHyperparametersSampler
from train_model.modules.configs.training import TrainingConfig
from train_model.modules.schemas.preprocessing import PreprocessOutputs
from train_model.modules.schemas.training import TrainModelOutputs
from train_model.modules.utilities.system import get_safe_cpu_count

def train_model(
    preprocess_outputs: PreprocessOutputs,
    scaler: type[RobustScaler],
    resampler: type[SMOTE],
    model: type[XGBClassifier],
    hyperparameters_sampler: type[XGBHyperparametersSampler],
) -> TrainModelOutputs:
    model_results = optimize_model_hyperparameters(
        preprocessed_output=preprocess_outputs,
        scaler=scaler,
        resampler=resampler,
        model=model,
        hyperparameters_sampler=hyperparameters_sampler,
    )

    best_model_hyperparameters = model_results.best_params
    best_model = Pipeline([
        (MLflowConfig.scaler_name, scaler()),
        (
            MLflowConfig.resampler_name,
            resampler(random_state=TrainingConfig.random_state),
        ),
        (
            MLflowConfig.model_name,
            model(
                **best_model_hyperparameters,
                scale_pos_weight=preprocess_outputs.original_y_train_positive_scale,
                random_state=TrainingConfig.random_state,
                n_jobs=get_safe_cpu_count(),
                verbosity=2,
            ),
        ),
    ]).fit(
        preprocess_outputs.x_train,
        preprocess_outputs.y_train,
    )

    return TrainModelOutputs(
        model=best_model,
        hyperparameters=best_model_hyperparameters,
    )

def optimize_model_hyperparameters(
    preprocessed_output: PreprocessOutputs,
    scaler: type[RobustScaler],
    resampler: type[SMOTE],
    model: type[XGBClassifier],
    hyperparameters_sampler: type[XGBHyperparametersSampler],
) -> Study:
    def objective(trial: optuna.Trial) -> float:
        estimator = Pipeline([
            (MLflowConfig.scaler_name, scaler()),
            (
                MLflowConfig.resampler_name,
                resampler(random_state=TrainingConfig.random_state),
            ),
            (
                MLflowConfig.model_name,
                model(
                    **hyperparameters_sampler().resolve(trial),
                    scale_pos_weight=preprocessed_output.original_y_train_positive_scale,
                    random_state=TrainingConfig.random_state,
                    n_jobs=get_safe_cpu_count(),
                    verbosity=2,
                ),
            ),
        ])

        model_score = float(
            numpy.mean(
                cross_val_score(
                    estimator,
                    preprocessed_output.x_train,
                    preprocessed_output.y_train,
                    cv=preprocessed_output.cross_validation,
                    scoring="average_precision",
                    n_jobs=1,
                )
            )
        )

        return model_score

    study = optuna.create_study(
        direction="maximize",
        sampler=TPESampler(
            seed=TrainingConfig.random_state,
        ),
    )
    study.optimize(
        objective,
        n_trials=TrainingConfig.bayes_steps,
        n_jobs=1,
        show_progress_bar=True,
        gc_after_trial=True,
        timeout=TrainingConfig.training_timeout_seconds,
    )

    return study