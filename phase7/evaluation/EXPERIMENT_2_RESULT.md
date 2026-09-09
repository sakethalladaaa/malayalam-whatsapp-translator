# Phase 7 — Experiment 2 Result

## Intervention

A conservative Roman Malayalam input-normalization layer was evaluated before IndicXlit.

Rules:

- `nale` -> `naale`
- `ariyamo` -> `ariyaamo`
- `inu` -> `innu`

Rules are applied only to complete Roman tokens.

No Phase 5 routing logic, IndicXlit model weights, beam width, or rescore setting was changed.

## Development Evaluation

The candidate was selected using the separate 20-sample Phase 7 development dataset.

| Metric | Raw IndicXlit | Candidate |
|---|---:|---:|
| Samples | 20 | 20 |
| Exact match | 30.00% | 40.00% |
| Mean normalized similarity | 90.60% | 92.15% |

Mean similarity improvement: **+1.55 percentage points**.

- Improved: 3
- Unchanged: 17
- Worsened: 0

The previously tested rule `evida` -> `evideyaa` was rejected because it caused a development-set regression.

## Fresh Holdout Evaluation

The candidate was evaluated once on the untouched 30-sample Phase 7 holdout.

| Metric | Raw IndicXlit | Normalized |
|---|---:|---:|
| Samples | 30 | 30 |
| Exact match | 43.33% | 46.67% |
| Mean normalized similarity | 93.98% | 94.34% |

Mean similarity improvement: **+0.36 percentage points**.

- Improved: 2
- Unchanged: 28
- Worsened: 0

Category mean similarity:

| Category | Raw | Normalized |
|---|---:|---:|
| control_conversational | 91.93% | 92.60% |
| mixed_chat | 93.92% | 93.92% |
| short_chat | 91.75% | 92.86% |
| social_chat | 94.40% | 94.40% |
| target_spelling | 97.92% | 97.92% |

## Holdout Improvements

### ID 8

Input:

`enikku nale exam undu`

Raw:

`എനിക്കു നാലെ എക്സാം ഉണ്ടു`

After normalization:

`എനിക്കു നാളെ എക്സാം ഉണ്ടു`

Ground truth:

`എനിക്ക് നാളെ പരീക്ഷ ഉണ്ട്`

Similarity improved from **0.720 to 0.760**.

### ID 18

Input:

`ariyamo?`

Raw:

`അറിയമോ?`

After normalization:

`അറിയാമോ?`

Ground truth:

`അറിയാമോ?`

Similarity improved from **0.933 to 1.000**.

## Interpretation

Experiment 2 provides evidence that a small Roman spelling-normalization layer can generalize to some unseen inputs.

The improvement is modest on the 30-sample holdout (+0.36 percentage points mean similarity), but there were no observed regressions.

The intervention does not solve broader transliteration weaknesses such as lexical ambiguity, mixed-language handling, slang, or general surface-form variation.

These results are project validation evidence, not a standardized benchmark and not evidence of semantic translation quality.

## Decision

The three normalization rules are retained as a controlled Phase 7 preprocessing candidate.

The 30-sample holdout is now considered evaluated and frozen. No additional rules should be selected by mining this holdout.

Any further Phase 7 experiment must use a separate development/evidence source and compare against the frozen raw IndicXlit baseline.
