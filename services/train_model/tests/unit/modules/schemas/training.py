from services.train_model.src.modules.schemas.training import TrainModelOutputs

class TestMLflowRegisteredModelInfo:
    @staticmethod
    def data() -> dict:
        return {
            "model": object(),
            "hyperparameters": {},
        }

    def test_values(self, data: dict):
        values = TrainModelOutputs(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            if isinstance(expected, dict):
                assert expected == actual
            else:
                assert expected is actual