# Phase 7 — Experiment 1 Result

## Intervention

A conservative Malayalam post-transliteration normalization layer was evaluated after raw IndicXlit inference.

Rules:

- `ഇന്നു` -> `ഇന്ന്`
- `ഒന്നു` -> `ഒന്ന്`
- whole-token `ചെയ്യു` -> `ചെയ്യൂ`
- `വിളിക്കം` -> `വിളിക്കാം`

The `ചെയ്യു` rule is restricted to a complete token to avoid modifying longer forms such as `ചെയ്യുന്നെ` and `ചെയ്യുമോ`.

No Phase 5 routing logic, IndicXlit model weights, beam width, or rescore setting was changed.

## Frozen Phase 6 Evaluation

The existing 75-sample Phase 6 validation set was used only as historical evidence.

| Metric | Raw IndicXlit | Normalized |
|---|---:|---:|
| Samples | 75 | 75 |
| Exact match | 22 | 25 |
| Mean normalized similarity | 91.43% | 92.19% |
| Median normalized similarity | 94.74% | 95.87% |
| Improved | — | 14 |
| Unchanged | — | 61 |
| Worsened | — | 0 |

Mean similarity improvement: **+0.76 percentage points**.

The normalization rules therefore improve several known historical surface-form failures without causing a measured regression on this frozen set.

## Fresh Phase 7 Holdout

A separate 30-sample holdout was created before evaluating the intervention.

| Metric | Raw IndicXlit | Normalized |
|---|---:|---:|
| Samples | 30 | 30 |
| Exact match | 13 | 13 |
| Mean normalized similarity | 93.98% | 93.98% |
| Median normalized similarity | 96.72% | 96.72% |
| Improved | — | 0 |
| Unchanged | — | 30 |
| Worsened | — | 0 |

The four rules changed **0 of 30** fresh holdout outputs.

## Interpretation

Experiment 1 demonstrates that the normalization rules can correct recurring surface-form patterns observed in the historical Phase 6 failures.

However, the fresh Phase 7 holdout shows **no measurable improvement or regression**. Therefore the experiment does not provide evidence that this particular rule set generalizes broadly to unseen Roman Malayalam inputs.

The rules should not be expanded by mining the Phase 7 holdout, because that would turn the holdout into a tuning set.

## Decision

Experiment 1 is retained as a controlled, historical-evidence-backed intervention.

It should not be claimed as a generalized transliteration-quality improvement.

Further Phase 7 work requires a separately defined development/evidence source before introducing additional rules, such as broader lexical handling, English-token preservation, spelling normalization, or candidate reranking.

Character similarity remains a surface-form metric and does not establish semantic meaning preservation.
