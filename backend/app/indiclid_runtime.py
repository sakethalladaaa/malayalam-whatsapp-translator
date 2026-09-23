"""Lazy production loader for the validated AI4Bharat IndicLID runtime."""

from __future__ import annotations

import importlib.util
import os
from functools import lru_cache
from pathlib import Path
from threading import Lock
from typing import Any

from backend.app.lid import IndicLIDUnavailableError

_INIT_LOCK = Lock()

_REQUIRED_FILES = (
    "IndicLID.py",
    "models/indiclid-ftn/model_baseline_roman.bin",
    "models/indiclid-ftr/model_baseline_roman.bin",
    "models/indiclid-bert/basline_nn_simple.pt",
)


@lru_cache(maxsize=1)
def _load_engine(inference_dir: str) -> Any:
    directory = Path(inference_dir)

    try:
        for relative_path in _REQUIRED_FILES:
            if not (directory / relative_path).is_file():
                raise FileNotFoundError(
                    f"IndicLID runtime file missing: {relative_path}"
                )

        from transformers import BertConfig, BertForSequenceClassification

        spec = importlib.util.spec_from_file_location(
            "_phase9_upstream_indiclid",
            directory / "IndicLID.py",
        )
        if spec is None or spec.loader is None:
            raise ImportError("Cannot import the IndicLID inference module.")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Upstream IndicLID uses relative model paths during initialization.
        with _INIT_LOCK:
            previous_directory = Path.cwd()
            try:
                os.chdir(directory)
                model = module.IndicLID(
                    input_threshold=0.5,
                    roman_lid_threshold=0.6,
                )
            finally:
                os.chdir(previous_directory)

        # Reconstruct the legacy BERT checkpoint for current Transformers.
        old_model = model.IndicLID_BERT
        new_config = BertConfig(**vars(old_model.config))
        new_model = BertForSequenceClassification(new_config)

        load_result = new_model.load_state_dict(
            old_model.state_dict(),
            strict=False,
        )
        allowed_difference = {"bert.embeddings.position_ids"}

        if (
            set(load_result.missing_keys) - allowed_difference
            or set(load_result.unexpected_keys) - allowed_difference
        ):
            raise RuntimeError("IndicLID BERT checkpoint weights do not match.")

        model.IndicLID_BERT = new_model.to(model.device).eval()
        return model

    except Exception as exc:
        raise IndicLIDUnavailableError(
            "IndicLID model/runtime failed to initialize."
        ) from exc


def get_indiclid_engine() -> Any | None:
    """Return the cached model, or None when IndicLID is not configured."""
    configured_path = os.environ.get("INDICLID_INFERENCE_DIR")

    if not configured_path:
        return None

    inference_dir = str(Path(configured_path).expanduser().resolve())
    return _load_engine(inference_dir)
