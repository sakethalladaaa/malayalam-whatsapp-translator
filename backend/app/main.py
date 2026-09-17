from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from backend.app.indictrans2_runtime import get_indictrans2_engine
from backend.app.indicxlit_runtime import get_indicxlit_engine
from backend.app.pipeline import (
    MixedTextUnsupportedError,
    TranslationPipeline,
)
from backend.app.translator import (
    IndicTrans2,
    IndicTrans2UnavailableError,
)
from backend.app.transliterator import (
    IndicXlit,
    IndicXlitUnavailableError,
)

app = FastAPI(
    title="Malayalam WhatsApp Translator API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Text cannot be empty.")

        return value


class TranslateResponse(BaseModel):
    input: str
    language: str
    translation: str | None


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/translate", response_model=TranslateResponse)
def translate(request: TranslateRequest) -> TranslateResponse:
    try:
        transliterator = IndicXlit(
            engine=get_indicxlit_engine(),
        )

        translator = IndicTrans2(
            engine=get_indictrans2_engine(),
        )

        pipeline = TranslationPipeline(
            transliterator=transliterator,
            translator=translator,
        )

        result = pipeline.process(request.text)

        return TranslateResponse(
            input=request.text,
            language=result.route,
            translation=result.translation,
        )

    except IndicTrans2UnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except IndicXlitUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except MixedTextUnsupportedError as exc:
        raise HTTPException(
            status_code=501,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc