from train_model.modules.configs.training import TrainingConfig
from train_model.services.initialization import seed_everything

def test_seed_everything():
    seed_everything(TrainingConfig.random_state)