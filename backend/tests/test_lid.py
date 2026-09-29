import pytest

from backend.app.lid import IndicLID, IndicLIDUnavailableError


def test_empty_text_is_rejected():
    with pytest.raises(ValueError):
        IndicLID().predict("")


def test_unconfigured_runtime_is_explicit():
    with pytest.raises(IndicLIDUnavailableError):
        IndicLID().predict("നമസ്കാരം")


def test_inference_failure_is_reported_as_unavailable():
    class FailingEngine:
        def batch_predict(self, texts, batch_size):
            raise RuntimeError("Model inference crashed.")

    with pytest.raises(
        IndicLIDUnavailableError,
        match="IndicLID inference failed",
    ):
        IndicLID(model=FailingEngine()).predict("Njan innu busy aanu")


@pytest.mark.parametrize(
    "prediction",
    [None, [], [()], [("text", "mal_Latn")], ["invalid"]],
)
def test_malformed_prediction_is_rejected(prediction):
    class MalformedEngine:
        def batch_predict(self, texts, batch_size):
            return prediction

    with pytest.raises(
        IndicLIDUnavailableError,
        match="unexpected prediction format",
    ):
        IndicLID(model=MalformedEngine()).predict("Njan innu busy aanu")
