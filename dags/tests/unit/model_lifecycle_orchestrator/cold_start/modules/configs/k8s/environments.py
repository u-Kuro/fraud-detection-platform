from dags.model_lifecycle_orchestrator.cold_start.modules.configs.k8s.environments import SeedTransactionInferencesEnvironmentKeys

class TestSeedTransactionInferencesEnvironmentKeys:
    def test_identity(self):
        from enum import StrEnum
        assert issubclass(SeedTransactionInferencesEnvironmentKeys, StrEnum)
    
    def test_transaction_inferences_seed_s3_key(self):
        assert SeedTransactionInferencesEnvironmentKeys.TRANSACTION_INFERENCES_SEED_S3_KEY == "TRANSACTION_INFERENCES_SEED_S3_KEY"