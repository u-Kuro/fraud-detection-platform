from services.dags.train_model.src.modules.configs.training import TrainingConfig
from services.dags.train_model.src.services.initialization import seed_everything

def test_seed_everything():
    seed_everything(TrainingConfig.random_state)