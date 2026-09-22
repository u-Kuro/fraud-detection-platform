import numpy
from pytest_mock import MockerFixture

from train_model.src.services.evaluation import get_predictions_sklearn, evaluate_model_predictions, visualize_model_predictions

def test_get_predictions_sklearn(mocker: MockerFixture):
    y_prob = 1.0
    threshold = 0.5

    mock_model = mocker.MagicMock()
    mock_model.predict_proba.return_value = numpy.array([
        [1.0 - y_prob, y_prob]
    ])

    result = get_predictions_sklearn(
        model=mock_model,
        x=numpy.array([]),
        threshold=threshold
    )

    assert numpy.array_equal(result["y_prob"], [y_prob])
    assert numpy.array_equal(result["y_pred"], [int(y_prob >= threshold)])

def test_evaluate_model_predictions():
    data = numpy.array([0, 1])
    evaluate_model_predictions(
        y_pred=data,
        y_prob=data,
        y_true=data,
    )

def test_visualize_model_predictions():
    data = numpy.array([0, 1])
    visualize_model_predictions(
        title="value",
        y_pred=data,
        y_prob=data,
        y_true=data,
    )