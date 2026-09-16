from matplotlib.figure import Figure
from pandas import DataFrame
from pyfakefs.fake_filesystem import FakeFilesystem
from pyfakefs.fake_filesystem_unittest import Pause

from services.dags.train_model.src.repositories.mlflow.run import save_model_reference_dataset, save_model_metric_figures

def test_save_model_reference_data(fs: FakeFilesystem):
    with Pause(fs):
        save_model_reference_dataset(
            mlflow_model_run_id="value",
            model_reference_dataset=DataFrame()
        )

def test_save_model_metric_figures():
    save_model_metric_figures(
        model_metric_figures={
            "key": Figure()
        }
    )