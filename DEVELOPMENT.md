# Development Guide

## Project Purpose

Malayalam WhatsApp Translator is an open-source Chrome extension for WhatsApp Web that detects Malayalam text, including Romanized Malayalam (Manglish), and provides an English meaning.

The project is NOT an AI summarizer or chatbot.

## Development Stack

### Chrome Extension
- Manifest V3
- JavaScript
- HTML/CSS
- WhatsApp Web content scripts

### Backend
- Python 3.11+
- FastAPI
- Uvicorn

### AI / NLP
- AI4Bharat IndicLID — Malayalam and Roman Malayalam identification
- AI4Bharat IndicXlit — transliteration when required
- AI4Bharat IndicTrans2 — Malayalam to English translation

IndicLID experimentation and model validation are being performed in Google Colab before integration into the FastAPI backend.

## Project Architecture

```text
WhatsApp Web
      ↓
Chrome Extension
      ↓
Selected / Detected Text
      ↓
FastAPI Backend
      ↓
IndicLID
      ↓
If Malayalam
      ↓
IndicTrans2
      ↓
English Meaning
