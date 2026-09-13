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
```

## Current Implemented Architecture

```text
WhatsApp Web
      ↓
Chrome Extension
      ↓
Selected / Detected Message
      ↓
FastAPI Backend
      ↓
Language Identification + Routing
      ↓
English ─────────────────→ Leave unchanged
      ↓
Malayalam-family
      ├── Native Malayalam ─────→ IndicTrans2 → English meaning
      ├── Roman Malayalam ──────→ Roman normalization → IndicXlit
      │                           → Malayalam normalization → IndicTrans2
      └── Mixed Malayalam-English → Malayalam-aware routing → Translation
```

Phase 4 established the WhatsApp Web integration. The extension handles text selection, verifies that a selection belongs to a single WhatsApp message container, and sends the selected text to the local FastAPI endpoint.

WhatsApp-specific DOM selectors are isolated in `extension/src/whatsapp/dom.js`, while general extension interaction remains in `extension/src/content.js`.

## Phase 5 Validation Summary

Phase 5 was developed primarily in Google Colab before backend integration. IndicLID was evaluated on Native Malayalam, Roman Malayalam, Mixed Malayalam-English, and English WhatsApp-style messages.

The final balanced validation set contained 100 samples:

- 25 Native Malayalam
- 25 Roman Malayalam
- 25 Mixed Malayalam-English
- 25 English

The frozen `candidate_v1` router achieved:

| Metric | Result |
|---|---:|
| Accuracy | 97.00% |
| Precision | 100.00% |
| Recall | 96.00% |
| F1 | 97.96% |
| English false positives | 0 / 25 |

The final three Malayalam-family misses were retained for future analysis rather than tuned away.

## Phase 6 and Phase 7 Validation Summary

Phase 6 evaluated IndicXlit on 75 manually authored Roman Malayalam and
WhatsApp-style samples. The recorded baseline achieved 29.33% exact match and
91.43% mean normalized character similarity. These are project metrics, not a
standardized benchmark, and character similarity does not measure semantic
translation quality.

Phase 7 evaluated two conservative preprocessing interventions. Malayalam
post-transliteration normalization changed none of the 30 fresh holdout
outputs. Roman input normalization improved the recorded holdout from 43.33%
to 46.67% exact match and from 93.98% to 94.34% mean similarity, with no
observed regressions in that evaluation.

Phase 7 boundary regression tests cover longer Malayalam words, punctuation,
complete Roman tokens, case preservation, and empty input. The current
preprocessing tests pass 10/10 locally. The Phase 7 holdout and historical
result files remain frozen.

## Current Integration Boundary

Phase 5 routing, Phase 6 transliteration, and Phase 7 preprocessing have
validated evaluation artifacts. The backend still returns a scaffold response.
IndicLID model loading, IndicXlit invocation, IndicTrans2 translation, and
full end-to-end NLP wiring are Phase 8 work.

## Development Principles

1. Validate AI behavior before production integration.

2. Prefer small, measurable changes over broad rewrites.
3. Treat real WhatsApp-style spelling and code-switching as first-class test cases.
4. Freeze final validation rules before measuring final performance.
5. Keep large model binaries and temporary experimentation files out of Git.

6. Document failures and evaluation-harness issues instead of hiding them.
