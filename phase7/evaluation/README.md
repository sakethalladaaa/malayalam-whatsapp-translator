# Phase 7 — Roman Malayalam Preprocessing

## Scope

Evaluate two separate normalization interventions around IndicXlit:

- Experiment 1: Roman input -> raw IndicXlit -> Malayalam output normalization.
- Experiment 2: Roman input -> Roman token normalization -> IndicXlit.

See `EXPERIMENT_1_RESULT.md`, `EXPERIMENT_2_DEV_RESULT.md`, and
`EXPERIMENT_2_RESULT.md` for the historical evaluations.

The experiments do not establish the quality of applying both interventions
together.

Phase 5 candidate_v1 remains frozen. Phase 6 raw IndicXlit behavior remains
the baseline. No model weights or inference settings are changed.

## Experiments

Experiment 1 used four Malayalam surface-form corrections derived from
historical Phase 6 failure evidence. It changed none of the 30 Phase 7
holdout outputs.

Experiment 2 used three complete-token Roman rules selected on a separate
20-sample development set: `nale` -> `naale`, `ariyamo` -> `ariyaamo`, and
`inu` -> `innu`. The rule `evida` -> `evideyaa` was rejected after a
development regression.

No slang lexicon, candidate reranking, or English-token preservation strategy
was added.

## Evaluation Policy

- Existing Phase 6 75-sample validation set is frozen and must not be used for tuning.
- Phase 7 requires a fresh holdout dataset.
- Compare preprocessing against the unchanged raw IndicXlit baseline on the same fresh holdout.
- Report exact match and normalized character similarity.
- Report category-level results where categories are available.
- Character similarity is a surface metric, not a semantic metric.

## Acceptance Criteria

A preprocessing change is considered promising only if it improves the fresh-holdout baseline on the targeted spelling/short-chat cases without causing material regression on the remaining cases.

## Post-experiment Boundary Fix

After the recorded experiments, regression tests exposed two implementation
issues:

- Substring replacement corrupted longer words, such as `ഒന്നും`.
- The whitespace-only boundary left standalone `ചെയ്യു?` unchanged.

All four Malayalam rules now use a shared token boundary that includes word
characters, Malayalam Unicode characters, and ZWNJ/ZWJ joiners. This preserves
longer words while allowing the registered forms next to punctuation such as
question marks, commas, exclamation marks, and parentheses.

The rule dictionaries and Roman normalization behavior remain unchanged.
Roman rules remain case-sensitive.

Validation: 10 preprocessing unit tests passed locally. Coverage includes
existing Malayalam corrections, longer-word preservation, punctuation,
Roman token boundaries, case preservation, and empty/unchanged inputs.

This is a code-correctness fix, not a new transliteration-quality result.
Historical experiment reports and result CSVs describe the earlier
implementation; their metrics must not be attributed to this revised version.
No model evaluation was rerun for this fix, and the frozen datasets and
historical result files were not modified.

The evaluated Phase 7 holdout remains frozen. Any further candidate selection
requires separate development evidence; a fresh final evaluation set is needed
for new quality claims.
