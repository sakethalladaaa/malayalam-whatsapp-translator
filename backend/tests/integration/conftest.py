import os

import pytest


@pytest.fixture(scope="session")
def real_indicxlit_engine():
    if os.getenv("RUN_INDICXLIT_INTEGRATION") != "1":
        pytest.skip(
            "Real IndicXlit integration tests are disabled. "
            "Set RUN_INDICXLIT_INTEGRATION=1 to enable them."
        )

    os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")

    try:
        from backend.app.indicxlit_runtime import get_indicxlit_engine
        from backend.app.transliterator import IndicXlitUnavailableError
    except ImportError as exc:
        pytest.fail(
            f"IndicXlit production runtime loader could not be imported: {exc}",
            pytrace=True,
        )

    try:
        return get_indicxlit_engine()
    except IndicXlitUnavailableError as exc:
        pytest.fail(
            f"IndicXlit runtime/model failed to initialize: {exc}",
            pytrace=True,
        )
