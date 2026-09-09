# Phase 7 — Experiment 2 Development Result

## Intervention

A conservative Roman Malayalam input-normalization candidate was tested in memory before modifying the production/evaluation module.

Candidate rules:

- `nale` -> `naale`
- `ariyamo` -> `ariyaamo`
- `inu` -> `innu`

Rules are applied only as complete tokens.

## Development Set

- Samples: 20
- Dataset: `phase7/data/roman_malayalam_dev.csv`
- No overlap with Phase 6 validation
- No overlap with Phase 7 holdout

## Results

| Metric | Raw IndicXlit | Candidate |
|---|---:|---:|
| Samples | 20 | 20 |
| Exact match | 30.00% | 40.00% |
| Mean normalized similarity | 90.60% | 92.15% |

Mean similarity improvement: **+1.55 percentage points**.

Per-sample comparison:

- Improved: 3
- Unchanged: 17
- Worsened: 0

## Candidate Decision

The three-rule candidate is retained for evaluation on the untouched Phase 7 holdout.

The previously tested rule:

- `evida` -> `evideyaa`

is rejected because it caused a development-set regression for `evida nee`.

No rule is added based on the Phase 7 holdout.

## Evaluation Status

The development result does not establish generalization.

The 30-sample Phase 7 holdout remains untouched and will be used once for final comparison after the candidate implementation is frozen.
