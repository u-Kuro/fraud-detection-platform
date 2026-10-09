from pandas import DataFrame
from sklearn.model_selection import train_test_split, StratifiedKFold

from shared.modules.schemas.postgres.transaction_inferences import TransactionInferences
from train_model.modules.configs.training import TrainingConfig
from train_model.modules.schemas.preprocessing import PreprocessOutputs

def preprocess(dataset: DataFrame) -> PreprocessOutputs:
    x = dataset.drop(TransactionInferences.is_fraud.key, axis=1).values
    y = dataset[TransactionInferences.is_fraud.key].values

    x_train, x_test, y_train, y_test = train_test_split(
        x, y,
        test_size=TrainingConfig.test_size,
        random_state=TrainingConfig.random_state,
        stratify=y
    )

    cross_validation = StratifiedKFold(
        n_splits=int(1 / TrainingConfig.cv_val_size),
        shuffle=True,
        random_state=TrainingConfig.random_state
    )

    return PreprocessOutputs(
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
        cross_validation=cross_validation
    )