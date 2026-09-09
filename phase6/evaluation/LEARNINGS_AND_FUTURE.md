# Phase 6 — Learnings, Engineering Decisions, and Future Use

## Purpose

Phase 6 evaluated AI4Bharat IndicXlit for Roman Malayalam / Manglish to Malayalam-script transliteration in WhatsApp-style messages.

The phase produced two kinds of outcomes:

1. Engineering problems that were resolved or mitigated so IndicXlit could be evaluated reproducibly.
2. Model limitations discovered during validation that should guide future preprocessing, routing, evaluation, and integration work.

This document records both so later phases do not repeat the same debugging or make unsupported assumptions about transliteration quality.

## 1. Engineering Issues and Techniques Used

### Python / dependency compatibility

**Issue:** The main project environment used Python 3.11, but the IndicXlit/Fairseq stack showed runtime compatibility problems during model loading.

**Technique used:** Created an isolated `.venv-indicxlit` environment with Python 3.10.21 instead of changing the main project environment.

**Learning:** Model-specific legacy dependencies should be isolated when they require a different runtime from the main application.

**Future use:** Keep research/model environments separate from the production application environment whenever dependency stacks are incompatible.

### Packaging / installer compatibility

**Issue:** The available pip version caused installation friction with the legacy IndicXlit dependency stack.

**Technique used:** Pinned pip to 24.0 inside the isolated environment and installed the required IndicXlit dependency stack there.

**Learning:** Exact dependency versions matter for reproducibility.

**Future use:** Record and preserve package versions instead of relying on latest versions.

### PyTorch / Fairseq checkpoint loading

**Issue:** The IndicXlit checkpoint did not load with the newer PyTorch checkpoint-loading behavior.

**Technique used:** Used the documented runtime compatibility setting:

`TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1`

The trusted published checkpoint was loaded without modifying model weights.

**Learning:** Legacy research models may require explicit runtime compatibility handling.

**Future use:** Keep compatibility settings documented and environment-specific rather than changing third-party model files.

### Inference wrapper API mismatch

**Issue:** `XlitEngine` is exposed as a factory function rather than behaving like a normal Python class. A class-style runtime type annotation caused a `TypeError`.

**Technique used:** Removed the incorrect runtime type annotation and kept the wrapper focused on engine creation and transliteration.

**Learning:** Third-party APIs should be verified through actual runtime behavior before adding assumptions around their types.

**Future use:** Keep wrappers small and verify external APIs before introducing strict typing assumptions.

### Repeated model initialization

**Issue:** Initializing the transliteration engine for every sample would introduce unnecessary overhead.

**Technique used:** Created one engine and reused it across the validation set.

**Learning:** Model lifecycle should be controlled explicitly during evaluation.

**Future use:** Reuse loaded model instances during batch evaluation and later backend inference where appropriate.

## 2. Evaluation Techniques Used

### Small seed before larger validation

A 12-sample seed set was first used to verify the complete input → transliteration → scoring pipeline.

Only after the pipeline worked was the larger validation set evaluated.

**Learning:** Validate the evaluation machinery before interpreting model metrics.

### Product-oriented validation categories

The final 75 samples were manually authored to represent realistic WhatsApp-style usage.

Categories included:

- short chat
- normal conversational Roman Malayalam
- informal/chat expressions
- spelling variation
- mixed Malayalam-English chat
- questions
- requests
- social/chat expressions
- longer messages

**Learning:** A WhatsApp-oriented product must evaluate messy conversational inputs rather than only clean textbook sentences.

### Multiple metrics

Two primary metrics were used:

- **Exact Match** for strict surface-form agreement.
- **Normalized Character Similarity** using `SequenceMatcher` for approximate surface closeness.

**Learning:** Roman Malayalam has spelling variation and transliteration ambiguity, so exact match alone can understate usefulness.

At the same time, character similarity is not a semantic metric and cannot prove meaning preservation.

### Category-wise analysis

The final results were analyzed by message category instead of reporting only one aggregate score.

**Learning:** Aggregate metrics can hide important product weaknesses. Category-level results help identify where preprocessing or model improvements are needed.

### Failure analysis without post-hoc tuning

The 22 samples below 0.90 similarity were preserved as a failure set and categorized.

No model weights, beam width, rescore setting, or Phase 5 `candidate_v1` router behavior were changed after observing the final validation results.

**Learning:** Validation evidence should remain frozen before tuning. Otherwise a validation set can gradually become a tuning set.

## 3. Problems Discovered That Were Not Fully Solved

### Short informal / colloquial expressions

Examples such as:

`shari` → `ഷാരി` instead of `ശരി`

`shari chetta` → `ഷാരി ചെറ്റ` instead of `ശരി ചേട്ടാ`

`enthanu?` → `എന്തന്?` instead of `എന്താണ്?`

**Learning:** Short conversational expressions are highly sensitive to phonetic and orthographic variation.

**Future use:** Consider dedicated normalization, lexical handling, or candidate selection for frequent short expressions.

### Roman spelling variation

Examples:

`nale` → `നാലെ`

`naale` → `നാളെ`

`evideya` → `എവിടെയ`

`evideyaa` → `എവിടെയാ`

**Learning:** Repeated vowels and conversational spelling conventions can materially affect transliteration.

**Future use:** Roman Malayalam normalization should become a first-class preprocessing problem.

### Orthographic / surface-form differences

Examples:

`innu` → `ഇന്നു` versus expected `ഇന്ന്`

`cheyyu` → `ചെയ്യു` versus expected `ചെയ്യൂ`

`vilikkam` → `വിളിക്കം` versus expected `വിളിക്കാം`

**Learning:** Some exact-match failures are small surface-form differences rather than complete transliteration failures.

**Future use:** Separate harmless orthographic variation from meaning-changing errors.

### Segmentation and hyphenation

Example:

`college-il` → `കോളേജ്-ഇൽ`

Expected project form:

`കോളേജിൽ`

**Learning:** Transliteration and morphological segmentation can produce different surface forms.

**Future use:** Evaluate conservative Malayalam-specific post-transliteration normalization rules.

### English fragments and abbreviations

Examples:

`pls vegam vaa` → `പിഎൽഎസ് വേഗം വാ`

`oru msg ayakku` → `ഒരു എംഎസ്ജി അയക്കു`

`okay alle?` → `ഒകയ് അല്ലെ?`

**Learning:** Mixed-language messages cannot always be handled by blindly transliterating every Latin token.

**Future use:** Preserve recognized English tokens and abbreviations where appropriate before transliteration.

### Slang and social expressions

Example:

`pwoli macha` → `പ്വോളി മച്ച`

**Learning:** Informal slang and social language remain difficult for generic transliteration.

**Future use:** Consider a curated conversational Malayalam/slang lexicon and candidate reranking for frequent expressions.

## 4. Final Phase 6 Evidence

The 75-sample project validation produced:

| Metric | Result |
|---|---:|
| Samples | 75 |
| Exact match | 29.33% |
| Mean normalized character similarity | 91.43% |
| Median normalized character similarity | 94.74% |
| Similarity >= 0.90 | 53/75 (70.67%) |
| Similarity < 0.90 | 22/75 (29.33%) |

These are **project validation results**, not a standardized benchmark and not evidence of semantic translation quality.

## 5. Decisions Carried Forward to Future Phases

### Preserve Phase 5 routing

IndicXlit is a downstream transliteration component and should not replace the Phase 5 language-identification and routing logic.

The existing `candidate_v1` router remains frozen unless future evidence demonstrates a concrete routing defect.

### Add transliteration-aware preprocessing carefully

Future experiments can evaluate:

1. Roman spelling normalization.
2. English-token and abbreviation preservation.
3. Common colloquial Malayalam lexicon handling.
4. Conservative punctuation and whitespace normalization.
5. Candidate generation and reranking for ambiguous short inputs.

Every improvement should be evaluated on a fresh holdout set rather than tuning only on the existing 75 samples.

### Separate script conversion from meaning preservation

Future phases should separately evaluate:

- language identification
- Roman Malayalam → Malayalam-script transliteration
- Malayalam → English translation
- final meaning preservation

A high character-similarity score cannot prove that the final translated meaning is correct.

### Prefer targeted improvements

The largest observed weaknesses are concentrated in:

- short informal chat
- spelling variation
- English abbreviations
- slang
- mixed-language input

Future engineering should therefore prioritize targeted preprocessing and quality checks before replacing the transliteration model wholesale.

### Preserve reproducibility

The project should retain:

- isolated environment information
- pinned package versions
- runtime compatibility configuration
- inference wrapper
- evaluation script
- validation datasets
- result CSV files
- failure analysis
- engineering learnings

This allows future model comparisons without rebuilding the setup from memory.

## 6. Phase 6 Takeaway

**IndicXlit successfully provides a usable Roman Malayalam → Malayalam-script capability, but raw transliteration is not sufficient by itself for production WhatsApp chat.**

The key engineering lesson is that the quality problem is not only model selection. It is also an input-normalization, code-switching, spelling-variation, conversational-lexicon, and evaluation-design problem.

Future phases should build on the frozen Phase 5 router and the Phase 6 evidence, adding targeted preprocessing and quality checks only when supported by fresh validation.
