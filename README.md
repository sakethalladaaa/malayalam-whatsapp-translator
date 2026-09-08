# Malayalam WhatsApp Translator

An open-source Chrome extension designed to help users understand Malayalam messages on WhatsApp Web by detecting Malayalam text and translating it into English.

## Project Overview

The project focuses on Malayalam messages written in:

- Native Malayalam script
- Romanized Malayalam (Manglish)
- Mixed Malayalam-English WhatsApp messages

The core workflow is:

**Select or detect message → Identify Malayalam → Translate Malayalam to English → Show English meaning**

English messages should remain unchanged.

> This project is not an AI summarizer or chatbot. The primary goal is Malayalam language identification and Malayalam-to-English translation.

## Problem

Users who do not understand Malayalam may receive Malayalam or Roman Malayalam messages in WhatsApp chats.

Native Malayalam script can be difficult to understand, while Roman Malayalam is harder for conventional language identification systems because it uses Latin characters and often contains English words.

## Proposed Solution

A Chrome extension for WhatsApp Web will detect Malayalam text and provide an English meaning without changing normal English messages.

Example Roman Malayalam messages:

```text
Athrem onnum venda
Enikku manasilayi
Ningal evideya
Njan innu busy aanu
```

## Development Tools

The project uses the following development tools and open-source technologies.

| Tool / Technology | Purpose | Official Link |
|---|---|---|
| Python 3.11+ | Backend development | https://www.python.org/downloads/ |
| Git | Version control | https://git-scm.com/ |
| Google Chrome | Chrome extension testing | https://www.google.com/chrome/ |
| Visual Studio Code | Development environment | https://code.visualstudio.com/ |
| FastAPI | Backend API framework | https://fastapi.tiangolo.com/ |
| Uvicorn | ASGI server for FastAPI | https://www.uvicorn.org/ |
| AI4Bharat IndicLID | Indian language identification | https://github.com/AI4Bharat/IndicLID |
| AI4Bharat IndicXlit | Indic transliteration | https://github.com/AI4Bharat/IndicXlit |
| AI4Bharat IndicTrans2 | Indic language translation | https://github.com/AI4Bharat/IndicTrans2 |

### Recommended Environment

- Python 3.11 or newer
- Google Chrome
- Git
- Visual Studio Code
- macOS / Windows / Linux

## Project Status

| Phase | Scope | Status |
|---|---|---|
| Phase 0 | Git repository and project setup | ✅ Complete |
| Phase 1 | Backend foundation | ✅ Complete |
| Phase 2 | Chrome extension popup UI | ✅ Complete |
| Phase 3 | Extension → FastAPI communication | ✅ Complete |
| Phase 4 | WhatsApp Web DOM integration | ✅ Complete |
| Phase 5 | IndicLID evaluation and Malayalam routing | ✅ Complete |
| Phase 6 | IndicXlit transliteration | ⬜ Next |

## Current Architecture

```text
WhatsApp Web
      ↓
Chrome Extension
      ↓
Selected / detected message
      ↓
Language identification + routing
      ↓
English ─────────────────→ Leave unchanged
      ↓
Malayalam-family
      ├── Native Malayalam ─────→ Translation path
      ├── Roman Malayalam ──────→ IndicXlit → Translation
      └── Mixed Malayalam-English → Malayalam-aware routing
