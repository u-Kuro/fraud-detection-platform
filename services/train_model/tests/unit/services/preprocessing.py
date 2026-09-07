from pandas import DataFrame

from services.shared.src.modules.schemas.postgres.transaction_inferences import TransactionInferences
from services.train_model.src.services.preprocessing import preprocess

def test_preprocess():
    number_of_class = 2
    minimum_sample_per_class = 3
    data = DataFrame({
        "feature": [1] * number_of_class * minimum_sample_per_class,
        TransactionInferences.is_fraud.key: [0] * minimum_sample_per_class + [1] * minimum_sample_per_class
    })

    preprocess(dataset=data)

