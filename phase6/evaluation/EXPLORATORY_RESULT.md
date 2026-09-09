# Phase 6 — Exploratory Evaluation Note

The 50-sample IndicXlit evaluation is exploratory and is not used as a tuned development set.

The model configuration was kept fixed during evaluation:
XlitEngine(src_script_type="roman", beam_width=10, rescore=False)

No model weights or inference parameters were changed after observing the results.

Observed exploratory result:
- 50 samples
- Exact-match rate: 30.00%
- Mean normalized character similarity: 92.60%
- Median normalized similarity: 95.12%
- 39/50 samples reached >= 0.90 normalized similarity

The observed failures are retained for failure analysis rather than used to tune the model.
