from dataclasses import fields
from types import FunctionType
from typing import TypeAliasType

import optuna

from train_model.modules.configs.hyperparameters import XGBHyperparametersSampler

class TestXGBHyperparametersSampler:
    def test_values(self):
        assert isinstance(XGBHyperparametersSampler.HyperparameterSampler, TypeAliasType)
        for field in fields(XGBHyperparametersSampler):
            assert getattr(XGBHyperparametersSampler, field.name)
        assert isinstance(XGBHyperparametersSampler.resolve, FunctionType)

    def test_resolve(self):
        trial = optuna.create_study().ask()
        resolved = XGBHyperparametersSampler().resolve(trial)
        field_names = {field.name for field in fields(XGBHyperparametersSampler)}

        assert all(name in resolved for name in field_names)
        assert all(isinstance(value, (int, float)) for value in resolved.values())