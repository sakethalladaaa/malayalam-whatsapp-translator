from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Malayalam WhatsApp Translator API",
    version="0.1.0",
)


class TranslateRequest(BaseModel):
    text: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/translate")
def translate(request: TranslateRequest):
    return {
        "input": request.text,
        "language": "unknown",
        "translation": None,
    }
