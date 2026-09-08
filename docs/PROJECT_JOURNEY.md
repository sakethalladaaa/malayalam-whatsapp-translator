# Project Journey — Malayalam WhatsApp Translator

## 1. Project Goal

Malayalam WhatsApp Translator is a lightweight Chrome extension intended to help users understand Malayalam messages received through WhatsApp Web.

The project supports three Malayalam-related input forms:
- Native Malayalam
- Roman Malayalam / Manglish
- Mixed Malayalam-English

Normal English messages should remain unchanged.

The project is developed as a real-world integration project. The browser extension, backend, language identification, routing, transliteration, and translation stages are developed and validated incrementally.

## 2. Development Phases

```text
Phase 0 → Project setup
Phase 1 → Backend foundation
Phase 2 → Chrome extension UI
Phase 3 → Extension ↔ FastAPI
Phase 4 → WhatsApp Web DOM integration
Phase 5 → IndicLID + routing validation
Phase 6 → IndicXlit transliteration
Phase 7 → IndicTrans2 translation integration
Phase 8 → End-to-end product validation
```

Phase 0 through Phase 5 are complete. Phase 6 is the next development stage.

## 3. Phase 0 — Project Setup

The project repository and development structure were established first so implementation could proceed with version control and a stable workspace.

### Engineering lesson

Version control was treated as part of the engineering process rather than something added after development.

## 4. Phase 1 — Backend Foundation

A FastAPI backend was created as the integration boundary between the browser extension and the AI pipeline.

The backend established:
- FastAPI application structure
- `/health` endpoint
- `/translate` endpoint
- request validation
- response models
- CORS configuration

At this stage the translation implementation was intentionally a scaffold.

### Engineering lesson

The backend contract was established before model integration so AI experimentation could happen independently from browser integration.

## 5. Phase 2 — Chrome Extension UI

A Chrome Manifest V3 extension scaffold and translation popup UI were implemented.

The extension provides the browser-side interaction required to select text and request a translation.

### Engineering lesson

The UI and backend were kept separate so model experimentation would not require repeatedly changing the browser layer.

## 6. Phase 3 — Extension to FastAPI

The extension was connected to the FastAPI backend.

The browser sends selected text to the local translation endpoint and displays the returned result.

### Engineering lesson

This established the first complete browser-to-backend path, making later AI integration possible without redesigning the extension communication layer.

## 7. Phase 4 — WhatsApp Web DOM Integration

Phase 4 connected the extension to actual WhatsApp Web message interaction.

The extension:
1. Detects selected text.
2. Determines whether the selection belongs to a WhatsApp message.
3. Prevents selections spanning multiple message containers.
4. Displays the translator popup.
5. Sends the selected text to the FastAPI backend.

WhatsApp-specific DOM handling was isolated into:

`extension/src/whatsapp/dom.js`

while general extension behavior remains in:

`extension/src/content.js`

### Challenge

WhatsApp Web is a dynamic web application, so DOM structure and message-container handling must be treated carefully.

### Solution

WhatsApp-specific selectors and message-container logic were isolated from general translation interaction code.

### Engineering lesson

Separating application logic from platform-specific DOM logic makes future changes safer.

## 8. Phase 5 — IndicLID Evaluation

Phase 5 was the first major AI validation stage. The goal was to determine whether IndicLID could reliably identify Native Malayalam, Roman Malayalam, Mixed Malayalam-English, and English WhatsApp-style messages before backend integration.

Experiments were performed primarily in Google Colab.

### IndicLID Configuration

- Input threshold: `0.5`
- Roman LID threshold: `0.6`
- Classes: `47`
- Native Malayalam: `mal_Mlym`
- Roman Malayalam: `mal_Latn`
- English: `eng_Latn`

## 9. IndicLID Challenges

### Roman Malayalam confusion

Roman Malayalam uses Latin characters, making short conversational messages difficult to distinguish from English and other Indic languages.

Examples of incorrect predictions included:

`nee food kazhicho?` → `guj_Latn`
`shari chetta 😄` → `tel_Latn`
`entha paripadi?` → `tel_Latn`
`evideya?` → `kan_Latn`
`varunundo?` → `tel_Latn`
`shari` → `snd_Latn`

### Mixed-language confusion

Code-switched messages also produced incorrect predictions, including:

`nale class undo?` → `tel_Latn`
`assignment ready aayo?` → `urd_Latn`
`project ready aayo?` → `guj_Latn`
`ipo busy aano?` → `san_Latn`
`okay alle?` → `san_Latn`
`sure aano?` → `ben_Latn`

### Engineering conclusion

IndicLID was useful, but model-only routing was not sufficient for realistic short Roman Malayalam and mixed WhatsApp messages.

## 10. IndicLID BERT Compatibility Challenge

The legacy IndicLID BERT checkpoint initially produced compatibility errors with the modern Transformers runtime.

### Solution

A runtime-only compatibility patch was applied to the loaded model. The official checkpoint weights were not modified.

The runtime was kept stable rather than repeatedly downgrading packages after a working configuration was established.

### Engineering lesson

Older research checkpoints may require compatibility handling when used with newer ML library internals.

## 11. IndicLID API Discovery

The official evaluation path required:

`lid.batch_predict([text], 1)`

Rather than assuming that `lid.predict(text)` would return the required prediction value directly.

### Engineering lesson

External model APIs should be inspected and tested before evaluation code is built around them.

## 12. Roman Malayalam Fallback

A lightweight Malayalam-specific lexical fallback was evaluated to compensate for weaknesses in IndicLID.

The fallback searched for Malayalam-specific Roman lexical markers such as:

`njan`, `enikku`, `ninakku`, `nee`, `innu`, `ippo`, `nale`, `evide`, `entha`, `undo`, `aano`, `aayo`, `kazhicho`, `varunundo`, `paripadi`, `chetta`, `shari`, `alle`, `aan`, `vilikkam`, `varam`, `cheytho`, `pokunnu`

The frozen rule was:

- Up to 4 words → at least 1 marker hit
- More than 4 words → at least 2 marker hits

The fallback was treated as an experimental candidate and validated rather than assumed to be production-ready.

## 13. Candidate Router v1

The final routing candidate combined IndicLID prediction with the Malayalam lexical fallback.

Malayalam processing was selected when:

- IndicLID predicted `mal_Mlym`, or
- IndicLID predicted `mal_Latn`, or
- the frozen Roman Malayalam fallback detected sufficient Malayalam-specific markers.

English protection remained enabled.

The candidate router was frozen before the final validation.

## 14. Evaluation-Harness Bug

During final evaluation, the fallback function returned `(detected, hits)` rather than a single Boolean.

An intermediate evaluation mistakenly treated the tuple itself as the routing Boolean. This produced an incorrect result where every English sample appeared to be routed to Malayalam.

### How it was detected

The unexpected result conflicted with earlier validation runs, which had shown zero English false positives.

The fallback implementation was inspected directly and its return structure was identified.

### Fix

The evaluation function was corrected to extract the detection value:

```python
detected, hits = roman_malayalam_fallback(text)
return detected
```

The routing rules themselves were not changed.

### Engineering lesson

The evaluation harness is part of the experimental system and must be validated independently of the model.

## 15. Validation Progress

### Initial 60-sample evaluation

IndicLID product-level Malayalam-family routing:
- Accuracy: `73.33%`
- Precision: `100%`
- Recall: `68%`
- F1: `80.95%`

### Held-out 30-sample validation

Frozen candidate_v1:
- Accuracy: `90.0%`
- Precision: `100%`
- Recall: `85.0%`
- F1: `91.89%`
- English false positives: `0 / 10`

### Fresh stress test

Frozen candidate_v1:
- `29 / 30` correct
- Approx. `96.67%` routing accuracy
- Precision: `100%`
- Recall: `96.67%`
- English false positives: `0 / 10`

## 16. Final 100-Sample Validation

The final validation set was balanced:

- 25 Native Malayalam
- 25 Roman Malayalam
- 25 Mixed Malayalam-English
- 25 English

IDs: `301–400`

The final frozen candidate_v1 result was:

| Metric | Result |
|---|---:|
| Accuracy | **97.00%** |
| Precision | **100.00%** |
| Recall | **96.00%** |
| F1 | **97.96%** |
| English false positives | **0 / 25** |

Routing counts:

- Malayalam-family correctly routed: **72 / 75**
- Malayalam-family missed: **3 / 75**
- English correctly protected: **25 / 25**
- English false positives: **0 / 25**

## 17. Final Failure Analysis

### Failure 1

`vegam vaa`

Ground truth: Roman Malayalam
IndicLID: `pan_Latn`

### Failure 2

`നാളെ class online ആണോ?`

Ground truth: Mixed Malayalam-English
IndicLID: `eng_Latn`

### Failure 3

`എനിക്ക് assignment submit ചെയ്യണം.`

Ground truth: Mixed Malayalam-English
IndicLID: `kas_Latn`

### Decision

The three failures were retained as documented validation findings. The final router was not tuned against the final validation set.

## 18. What We Learned

### Model-only routing is not always enough

IndicLID was strong for Native Malayalam but less reliable for short Roman Malayalam and mixed-language messages. This motivated a lightweight fallback layer instead of relying on a single prediction.

### Real WhatsApp language is messy

Roman Malayalam includes spelling variation, abbreviations, informal expressions, very short messages, and English words inside Malayalam sentences. These are normal product inputs.

### Safety matters

For this application, incorrectly processing a normal English message is undesirable. English false positives were therefore tracked as an explicit product metric.

### Evaluation integrity matters

The fallback tuple bug demonstrated that a strong-looking metric is meaningless when the evaluation harness is incorrect. Model behavior and evaluation logic both need validation.

### Freeze before final testing

The routing rules were frozen before the final 100-sample evaluation. Final validation failures were documented rather than used for tuning.

### Reproducibility matters

Large model binaries and temporary Colab artifacts are kept out of Git. Lightweight datasets, results, methodology, and decisions are preserved instead.

## 19. Current Limitations

The final validation demonstrates strong routing behavior, but it does not prove perfect production performance.

The final dataset is manually constructed rather than a naturally collected production corpus.

The three retained failures show unresolved weaknesses in very short Roman Malayalam, mixed-script messages, and code-switched text.

Future testing should use broader and more naturally representative WhatsApp-style variation while maintaining privacy and responsible data handling.

## 20. Current Project Decision

Phase 5 is complete and candidate_v1 is frozen as the validated Malayalam routing candidate.

The final product-level result was 97.00% accuracy, 100.00% precision, 96.00% recall, and 97.96% F1, with 0/25 English false positives on the final balanced validation set.

## 21. Phase 6 — IndicXlit

The next AI stage is transliteration:

```text
Roman Malayalam
      ↓
IndicXlit
      ↓
Native Malayalam
      ↓
IndicTrans2
      ↓
English meaning
```

Phase 6 will first validate IndicXlit independently using realistic Roman Malayalam WhatsApp-style inputs before integrating it into FastAPI.

The evaluation should cover short messages, conversational spelling, informal chat language, spelling variation, and code-switching rather than only clean textbook examples.

## 22. Final Engineering Principle

Build incrementally, measure honestly, preserve failures, and integrate only validated components.
