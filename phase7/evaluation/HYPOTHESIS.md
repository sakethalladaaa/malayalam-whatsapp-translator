# Phase 7 — Experiment 1 Hypothesis

## Evidence Source

The first preprocessing hypothesis is derived only from the frozen Phase 6 failure analysis.

Phase 6 identified:
- short conversational expressions
- Roman spelling variation
- orthographic / surface-form differences
- segmentation / hyphenation
- English fragments and abbreviations
- slang / social expressions

## First Intervention

Test a conservative Malayalam post-transliteration normalization layer.

The intervention should target recurring Malayalam surface-form errors rather than rewriting Roman input globally.

Initial hypothesis:

1. A small, explicitly documented set of Malayalam surface-form normalization rules can correct recurring orthographic variants.
2. Rules should operate only on Malayalam-script output produced by IndicXlit.
3. Rules should be deterministic and reviewable.
4. No model weights, beam width, rescore configuration, or Phase 5 routing behavior will change.
5. English tokens and Roman input will not be rewritten in this first experiment.
6. No slang dictionary or candidate reranking will be introduced in Experiment 1.

## Evidence-Guided Candidate Families

The Phase 6 findings suggest investigating:
- common conversational surface forms
- vowel / ending normalization
- segmentation and hyphenation
- recurring short-expression forms

Any concrete rule must be justified by examples from the frozen Phase 6 evidence or by independently authored development data.

## Evaluation Rule

The Phase 7 holdout must not be used to invent or select individual rules.

Rules are designed from frozen prior evidence first, then evaluated once against the fresh holdout.

## Success Criteria

Compare:
- raw IndicXlit baseline
- IndicXlit + post-transliteration normalization

using the same fresh holdout.

Report:
- exact-match rate
- mean normalized character similarity
- median normalized similarity
- category-level mean similarity
- regression count versus raw baseline
- number of samples improved, unchanged, and worsened

Character similarity is a surface-form metric and is not a semantic metric.
