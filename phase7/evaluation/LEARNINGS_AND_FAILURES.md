# Phase 7 — Learnings, Failures, and Engineering Decisions

## Purpose

Phase 7 investigated whether lightweight preprocessing could improve
Roman Malayalam → Malayalam-script transliteration quality while preserving
the frozen Phase 5 routing logic and the raw IndicXlit baseline.

The phase focused on targeted, measurable improvements rather than replacing
IndicXlit or introducing a large rule-based system.

---

## 1. Starting Point

Phase 6 established that raw IndicXlit can generate Malayalam-script output
with high character-level similarity, but observed weaknesses remained in:

- short informal / colloquial expressions
- Roman spelling variation
- orthographic / surface-form differences
- English fragments and abbreviations
- slang / social expressions
- segmentation and hyphenation

Phase 6 also established that character similarity is a surface metric and
cannot prove semantic meaning preservation.

Phase 7 therefore treated transliteration quality as a separate problem from
language identification and translation.

---

## 2. Frozen Components

The following were intentionally kept unchanged:

- Phase 5 `candidate_v1` routing logic
- IndicXlit model weights
- IndicXlit beam width
- IndicXlit rescore configuration
- Phase 6 validation dataset as tuning data
- Phase 7 fresh holdout after its evaluation

The purpose was to isolate preprocessing effects from model or routing changes.

---

## 3. Experiment 1 — Malayalam Post-Transliteration Normalization

### Hypothesis

Some recurring Phase 6 failures could be corrected by deterministic
Malayalam-script surface-form normalization after IndicXlit.

### Rules Tested

- `ഇന്നു` → `ഇന്ന്`
- `ഒന്നു` → `ഒന്ന്`
- whole-token `ചെയ്യു` → `ചെയ്യൂ`
- `വിളിക്കം` → `വിളിക്കാം`

The rules were derived from frozen Phase 6 failure evidence.

### Frozen Phase 6 Evaluation

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

### Fresh Phase 7 Holdout

| Metric | Raw IndicXlit | Normalized |
|---|---:|---:|
| Samples | 30 | 30 |
| Exact match | 13 | 13 |
| Mean normalized similarity | 93.98% | 93.98% |
| Median normalized similarity | 96.72% | 96.72% |
| Improved | — | 0 |
| Unchanged | — | 30 |
| Worsened | — | 0 |

### Lesson

The rules successfully corrected known historical surface-form failures but
did not change any unseen holdout examples.

Therefore Experiment 1 was retained as a controlled historical correction,
but was not claimed as a generalized transliteration improvement.

---

## 4. Experiment 2 — Roman Malayalam Input Normalization

### Motivation

The fresh development evaluation showed that several failures originated
from Roman spelling ambiguity before IndicXlit inference.

A separate 20-sample development dataset was created without overlap with the
frozen Phase 6 validation set or the Phase 7 holdout.

### Candidate Rules

- `nale` → `naale`
- `ariyamo` → `ariyaamo`
- `inu` → `innu`

Rules were restricted to complete Roman tokens.

### Rejected Rule

The candidate:

- `evida` → `evideyaa`

was rejected.

On development data:

`evida nee`

produced the target:

`എവിടാ നീ`

but normalizing the input to:

`evideyaa nee`

caused a worse output for that example.

### Development Result

| Metric | Raw IndicXlit | Candidate |
|---|---:|---:|
| Samples | 20 | 20 |
| Exact match | 30.00% | 40.00% |
| Mean normalized similarity | 90.60% | 92.15% |

Mean similarity improvement: **+1.55 percentage points**.

- Improved: 3
- Unchanged: 17
- Worsened: 0

### Fresh Holdout Result

The candidate was then evaluated once on the untouched 30-sample holdout.

| Metric | Raw IndicXlit | Normalized |
|---|---:|---:|
| Samples | 30 | 30 |
| Exact match | 43.33% | 46.67% |
| Mean normalized similarity | 93.98% | 94.34% |

Mean similarity improvement: **+0.36 percentage points**.

- Improved: 2
- Unchanged: 28
- Worsened: 0

Category results:

| Category | Raw | Normalized |
|---|---:|---:|
| control_conversational | 91.93% | 92.60% |
| mixed_chat | 93.92% | 93.92% |
| short_chat | 91.75% | 92.86% |
| social_chat | 94.40% | 94.40% |
| target_spelling | 97.92% | 97.92% |

### Holdout Improvements

`enikku nale exam undu`

Raw:

`എനിക്കു നാലെ എക്സാം ഉണ്ടു`

After normalization:

`എനിക്കു നാളെ എക്സാം ഉണ്ടു`

Similarity:

`0.720 → 0.760`

---

`ariyamo?`

Raw:

`അറിയമോ?`

After normalization:

`അറിയാമോ?`

Similarity:

`0.933 → 1.000`

---

## 5. Important Failure Lessons

### Generic normalization can over-correct

Roman spelling normalization is not deterministic in the sense that one
Roman form always maps to one desired Malayalam surface form.

Example:

`evida` can reasonably lead to outputs corresponding to different
conversational surface forms.

A rule that improves one example can therefore hurt another.

### More rules are not automatically better

Experiment 2 improved with only three rules.

The rejected `evida` rule demonstrates why every new rule needs isolated
development evidence before being accepted.

### Short chat remains difficult

The fresh holdout showed meaningful remaining difficulty in short messages.

This is important because WhatsApp usage contains many short expressions where
small orthographic differences can affect exact surface agreement.

### Mixed-language messages remain unresolved

Experiment 2 produced no aggregate change for the mixed-chat category.

This supports the earlier Phase 6 observation that English fragments and
abbreviations require a different strategy from simple spelling normalization.

### Slang remains unresolved

Social/chat expressions were unchanged by the Experiment 2 intervention.

A future slang-oriented solution should therefore be evaluated separately
rather than hidden inside a generic normalization dictionary.

### Surface similarity is not semantic evaluation

The reported similarity metrics only measure character-level surface closeness.

They do not establish that the translated meaning is correct.

Semantic translation quality must be evaluated separately in a later phase.

---

## 6. Evaluation Design Learnings

The most important process improvement in Phase 7 was separating:

- development data
- frozen historical validation data
- fresh holdout data

The Phase 7 holdout was deliberately not used to invent or select new rules.

This prevents the final holdout from silently becoming a tuning set.

Future experiments should preserve the same separation.

---

## 7. Engineering Decisions

### Preserve the raw baseline

Raw IndicXlit remains the reference system against which preprocessing
changes are measured.

### Preserve Phase 5 routing

Phase 7 does not replace or modify `candidate_v1`.

Language identification and Roman transliteration remain separate stages.

### Prefer small deterministic changes

The experiments demonstrated that a small rule set can produce measurable
improvements without changing the underlying model.

This is preferable to a broad rewrite when evidence is limited.

### Keep preprocessing modular

Roman input normalization and Malayalam post-transliteration normalization
are maintained as separate concepts.

This makes later experiments easier to compare and revert.

### Preserve reproducibility

Important artifacts remain in Git:

- datasets
- preprocessing implementation
- evaluation results
- experiment documentation
- test coverage

Model caches and virtual environments remain outside Git.

---

## 8. Current Phase 7 Outcome

Phase 7 has demonstrated a limited but measurable benefit from targeted Roman
Malayalam preprocessing.

The strongest verified result is the Experiment 2 fresh-holdout comparison:

- Exact match: **43.33% → 46.67%**
- Mean normalized similarity: **93.98% → 94.34%**
- Regressions: **0**

This is project-level validation evidence only.

It is not a standardized benchmark and does not establish semantic translation
quality.

---

## 9. What Phase 7 Did Not Solve

Phase 7 did not fully solve:

- general Roman spelling normalization
- ambiguous Roman spellings
- short colloquial expressions
- slang
- English abbreviation preservation
- mixed-language token handling
- morphological segmentation
- semantic translation

These remain separate engineering problems.

---

## 10. Recommended Next Direction

Before expanding the normalization rule set further, the next phase should
prioritize integration and semantic evaluation rather than accumulating a
large hand-built dictionary.

The current architecture supports:

Roman Malayalam
→ optional Roman normalization
→ IndicXlit
→ optional Malayalam surface normalization
→ Malayalam → English translation
→ result presentation

Phase 8 should therefore focus on integrating and evaluating the actual
Malayalam → English translation stage while keeping the Phase 7 preprocessing
candidate and Phase 5 router as independently testable components.

