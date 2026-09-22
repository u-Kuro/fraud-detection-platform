import json
from uuid import uuid4, UUID

import pytest
from pydantic import ValidationError

from fraud_detection_api.src.modules.schemas.slack import TrainingValue, PromotionValue

class TestTrainingValue:
    @staticmethod
    def make_json_data(**overrides) -> dict:
        data = {
            "workflow_id": str(uuid4()),
            "should_train_for_promotion": True
        }
        data.update(overrides)
        return data

    def test_values(self):
        json_data = self.make_json_data()
        value = TrainingValue(**json_data)

        for key, expected in json_data.items():
            actual = getattr(value, key)

            match key:
                case "workflow_id":
                    assert UUID(expected) == actual
                case "should_train_for_promotion":
                    assert expected == actual
                case _:
                    raise ValueError(f"Unexpected key: {key}")

    def test_failure_for_extra_field(self):
        data = self.make_json_data(extra=0)
        with pytest.raises(ValidationError):
            TrainingValue(**data)

class TestPromotionValue:
    @staticmethod
    def make_json_data(**overrides) -> dict:
        data = {
            "workflow_id": str(uuid4())
        }
        data.update(overrides)
        return data

    def test_values(self):
        json_data = self.make_json_data()
        value = PromotionValue(**json_data)

        for key, expected in json_data.items():
            actual = getattr(value, key)

            match key:
                case "workflow_id":
                    assert UUID(expected) == actual
                case _:
                    raise ValueError(f"Unexpected key: {key}")

    def test_failure_for_extra_field(self):
        data = self.make_json_data(extra=0)
        with pytest.raises(ValidationError):
            PromotionValue(**data)