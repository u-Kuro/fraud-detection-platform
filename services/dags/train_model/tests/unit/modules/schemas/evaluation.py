import pytest
from matplotlib.figure import Figure

from services.dags.train_model.src.modules.schemas.evaluation import ModelEvaluationMetrics, ModelEvaluationFigures, EvaluateModelOutputs

class TestModelEvaluationMetrics:
    @staticmethod
    def make_metrics() -> dict:
        return {
            "f1_score": 1.0,
            "pr_auc": 1.0,
            "recall": 1.0,
            "precision": 1.0,
            "roc_auc": 1.0,
            "accuracy": 1.0,
        }

    def test_values(self):
        data = self.make_metrics()
        values = ModelEvaluationMetrics(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            if isinstance(expected, float):
                assert expected == pytest.approx(actual)
            else:
                assert expected == actual

class TestModelEvaluationFigures:
    @staticmethod
    def make_figures() -> dict:
        return {
            "probability_scatter": Figure(),
            "confusion_matrix": Figure(),
        }

    def test_values(self):
        data = self.make_figures()
        values = ModelEvaluationFigures(**data)

        for key, expected in data.items():
            actual = getattr(values, key)

            assert expected is actual

class TestEvaluateModelOutputs:
    def test_values(self):
        metrics = TestModelEvaluationMetrics.make_metrics()
        figures = TestModelEvaluationFigures.make_figures()
        values = EvaluateModelOutputs(
            metrics=ModelEvaluationMetrics(**metrics),
            metric_figures=ModelEvaluationFigures(**figures)
        )

        for key, expected in metrics.items():
            actual = getattr(values.metrics, key)

            if isinstance(expected, float):
                assert expected == pytest.approx(actual)
            else:
                assert expected == actual

        for key, expected in figures.items():
            actual = getattr(values.metric_figures, key)

            assert expected is actual