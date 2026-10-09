import pytest

from drift_check.modules.configs.evidently import EvidentlyConfig

class TestEvidentlyConfig:
    def test_values(self):
        assert isinstance(EvidentlyConfig.data_drift_key, str)
        assert isinstance(EvidentlyConfig.concept_drift_key, str)
        assert isinstance(EvidentlyConfig.drifted_key, str)
        assert isinstance(EvidentlyConfig.minimum_fraud_samples, int)
        assert isinstance(EvidentlyConfig.share_of_drifted_features_threshold, float)
        assert isinstance(EvidentlyConfig.average_precision_delta_threshold, float)

        assert EvidentlyConfig.minimum_fraud_samples >= 100
        assert 1.0 > EvidentlyConfig.share_of_drifted_features_threshold > 0.0
        assert EvidentlyConfig.average_precision_delta_threshold == pytest.approx(-0.1)