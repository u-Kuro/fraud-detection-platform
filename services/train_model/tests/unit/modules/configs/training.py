from services.train_model.src.modules.configs.training import TrainingConfig

class TestTrainingConfig:
    def test_values(self):
        assert isinstance(TrainingConfig.random_state, int)
        assert isinstance(TrainingConfig.test_size, float)
        assert isinstance(TrainingConfig.bayes_steps, int)
        assert isinstance(TrainingConfig.training_timeout_seconds, int)
        assert isinstance(TrainingConfig.cv_val_size, float)

        assert TrainingConfig.random_state > 0
        assert 1.0 > TrainingConfig.test_size > 0.0
        assert TrainingConfig.bayes_steps > 0
        assert TrainingConfig.training_timeout_seconds > 0
        assert TrainingConfig.cv_val_size > 0