from fraud_detection_api.src.modules.schemas.mlflow import DeployedModel

class TestDeployedModel:
    @staticmethod
    def make_model(**overrides) -> dict:
        data = {
            "model_name": "value",
            "model_version": 1
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_model()
        values = DeployedModel(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual