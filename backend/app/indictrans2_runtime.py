"""
Phase 9 — Production IndicTrans2 runtime loader.

Loads the validated AI4Bharat IndicTrans2 Malayalam-to-English model lazily
and reuses one initialized engine across backend requests.
"""

from __future__ import annotations

from functools import lru_cache

from backend.app.translator import IndicTrans2UnavailableError

MODEL_NAME = "ai4bharat/indictrans2-indic-en-dist-200M"
MODEL_REVISION = "eb9e49d81077cfc5311e82ff36d8c1fc11557b5d"

SOURCE_LANGUAGE = "mal_Mlym"
TARGET_LANGUAGE = "eng_Latn"


class IndicTrans2Engine:
    """Real Malayalam-to-English IndicTrans2 inference engine."""

    def __init__(self) -> None:
        try:
            import torch
            from IndicTransToolkit import IndicProcessor
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        except ImportError as exc:
            raise IndicTrans2UnavailableError(
                "IndicTrans2 runtime dependencies are not available."
            ) from exc

        try:
            self._torch = torch
            if torch.cuda.is_available():
                self._device = "cuda"
            elif torch.backends.mps.is_available():
                self._device = "mps"
            else:
                self._device = "cpu"

            self._tokenizer = AutoTokenizer.from_pretrained(
                MODEL_NAME,
                revision=MODEL_REVISION,
                trust_remote_code=True,
            )

            self._model = AutoModelForSeq2SeqLM.from_pretrained(
                MODEL_NAME,
                revision=MODEL_REVISION,
                trust_remote_code=True,
            ).to(self._device)

            self._model.eval()
            self._processor = IndicProcessor(inference=True)

        except (OSError, RuntimeError, ValueError) as exc:
            raise IndicTrans2UnavailableError(
                "IndicTrans2 model/runtime failed to initialize."
            ) from exc

    @property
    def device(self) -> str:
        return self._device

    def translate(self, text: str) -> str:
        batch = self._processor.preprocess_batch(
            [text],
            src_lang=SOURCE_LANGUAGE,
            tgt_lang=TARGET_LANGUAGE,
        )

        inputs = self._tokenizer(
            batch,
            truncation=True,
            padding="longest",
            return_tensors="pt",
        ).to(self._device)

        try:
            with self._torch.inference_mode():
                generated_tokens = self._model.generate(
                    **inputs,
                    use_cache=True,
                    min_length=0,
                    max_length=256,
                    num_beams=5,
                    num_return_sequences=1,
                )
        except RuntimeError as exc:
            raise IndicTrans2UnavailableError(
                "IndicTrans2 inference failed."
            ) from exc

        decoded = self._tokenizer.batch_decode(
            generated_tokens,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )

        translations = self._processor.postprocess_batch(
            decoded,
            lang=TARGET_LANGUAGE,
        )

        return translations[0]


@lru_cache(maxsize=1)
def get_indictrans2_engine() -> IndicTrans2Engine:
    """Load and cache one production IndicTrans2 engine."""
    return IndicTrans2Engine()
