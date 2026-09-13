from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import TranslateRequest, TranslateResponse


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


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/translate", response_model=TranslateResponse)
def translate(request: TranslateRequest) -> TranslateResponse:
    return TranslateResponse(
        input=request.text,
        language="unknown",
        translation=None,
    )
