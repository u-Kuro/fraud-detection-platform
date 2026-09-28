from _pytest.monkeypatch import MonkeyPatch

from seed_transaction_inferences.modules.environment.seed_transaction_inferences import SeedTransactionInferencesEnvironment

class TestDriftCheckEnvironment:
    def test_instance(self):
        from seed_transaction_inferences.modules.environment.seed_transaction_inferences import seed_transaction_inferences_environment

        assert isinstance(seed_transaction_inferences_environment, SeedTransactionInferencesEnvironment)

    def test_values(self, monkeypatch: MonkeyPatch):
        value = "value"
        monkeypatch.setenv(
            name="TRANSACTION_INFERENCES_SEED_S3_KEY",
            value=value
        )

        environment = SeedTransactionInferencesEnvironment()

        assert environment.TRANSACTION_INFERENCES_SEED_S3_KEY == value