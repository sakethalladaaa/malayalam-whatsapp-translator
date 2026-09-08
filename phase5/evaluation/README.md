# Phase 5 — IndicLID Evaluation and Routing

## Objective

Evaluate IndicLID for Native Malayalam, Roman Malayalam, Mixed Malayalam-English, and English WhatsApp-style messages, then validate a conservative Malayalam routing strategy.

## IndicLID Configuration

- Input threshold: 0.5
- Roman LID threshold: 0.6
- Classes: 47
- Native Malayalam: `mal_Mlym`
- Roman Malayalam: `mal_Latn`
- English: `eng_Latn`

## Frozen candidate_v1

Malayalam route is selected when:

1. IndicLID predicts `mal_Mlym` or `mal_Latn`, OR
2. The frozen Roman Malayalam lexical fallback detects sufficient Malayalam-specific markers.

Fallback rule:

- Text with up to 4 words: at least 1 marker hit
- Text with more than 4 words: at least 2 marker hits

English protection remains enabled.

## Final 100-Sample Validation

Balanced dataset:

- 25 Native Malayalam
- 25 Roman Malayalam
- 25 Mixed Malayalam-English
- 25 English
- IDs 301–400

### Frozen candidate_v1 result

- Accuracy: 97.00%
- Precision: 100.00%
- Recall: 96.00%
- F1: 97.96%
- English false positives: 0/25

### Confusion Matrix

| Ground Truth | Malayalam Route | English Route |
|---|---:|---:|
| Malayalam-family | 72 | 3 |
| English | 0 | 25 |

### Failure Analysis

1. `vegam vaa` — Roman Malayalam — predicted `pan_Latn`
2. `നാളെ class online ആണോ?` — Mixed — predicted `eng_Latn`
3. `എനിക്ക് assignment submit ചെയ്യണം.` — Mixed — predicted `kas_Latn`

The three misses are retained as validation findings. candidate_v1 was not tuned after the final evaluation.

## Validation Decision

candidate_v1 is frozen as the validated Phase 5 routing candidate.

The final validation prioritizes safe English protection while maintaining high Malayalam-family recall.
