from dags.model_lifecycle_orchestrator.cold_start.modules.schemas.airflow.tasks import DataSeeding

class TestTransactionInferencesSeed:
    @staticmethod
    def make_seed(**overrides) -> dict:
        data = {
            "s3_key": "value",
        }
        data.update(overrides)
        return data

    def test_values(self):
        data = self.make_seed()
        values = DataSeeding(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected == actual