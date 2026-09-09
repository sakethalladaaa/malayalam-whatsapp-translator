# Phase 7 — Roman Malayalam Preprocessing

## Scope

Evaluate a conservative Roman Malayalam preprocessing layer before IndicXlit.

Pipeline under test:

Roman Malayalam input -> raw IndicXlit -> Malayalam post-transliteration normalization

Phase 5 candidate_v1 remains frozen. Phase 6 raw IndicXlit behavior remains the baseline.

## First Experiment

The first experiment focuses on conservative Malayalam post-transliteration surface-form normalization using patterns observed in Phase 6.

No slang lexicon, candidate reranking, English-token preservation, or model changes are included unless fresh evidence justifies a later experiment.

## Evaluation Policy

- Existing Phase 6 75-sample validation set is frozen and must not be used for tuning.
- Phase 7 requires a fresh holdout dataset.
- Compare preprocessing against the unchanged raw IndicXlit baseline on the same fresh holdout.
- Report exact match and normalized character similarity.
- Report category-level results where categories are available.
- Character similarity is a surface metric, not a semantic metric.

## Acceptance Criteria

A preprocessing change is considered promising only if it improves the fresh-holdout baseline on the targeted spelling/short-chat cases without causing material regression on the remaining cases.
