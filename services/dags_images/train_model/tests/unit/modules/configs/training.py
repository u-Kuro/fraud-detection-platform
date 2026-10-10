from train_model.modules.configs.training import TrainingConfig

class TestTrainingConfig:
    def test_values(self):
        assert isinstance(TrainingConfig.random_state, int)
        assert isinstance(TrainingConfig.test_size, float)
        assert isinstance(TrainingConfig.model_scoring, str)
        assert isinstance(TrainingConfig.bayes_steps, int)
        assert isinstance(TrainingConfig.training_timeout_seconds, int)
        assert isinstance(TrainingConfig.cv_val_size, float)
        assert isinstance(TrainingConfig.device, str)

        assert TrainingConfig.random_state == 42
        assert 1.0 > TrainingConfig.test_size > 0.0
        assert TrainingConfig.model_scoring == "average_precision"
        assert TrainingConfig.bayes_steps > 0
        assert TrainingConfig.training_timeout_seconds > 0
        assert TrainingConfig.cv_val_size > 0
        assert TrainingConfig.device == "cuda" or TrainingConfig.device == "cpu"