# Phase 6 — IndicXlit Evaluation

## Objective

Evaluate AI4Bharat IndicXlit for Roman Malayalam / Manglish to Malayalam-script transliteration in realistic WhatsApp-style messages.

## Environment

- Python: 3.10.21
- pip: 24.0
- ai4bharat-transliteration: 1.1.3
- Fairseq: 0.12.2
- PyTorch: 2.14.0
- Platform: Apple Silicon macOS

## Inference Configuration

XlitEngine(src_script_type="roman", beam_width=10, rescore=False)

Malayalam inference uses engine.translit_sentence(text, lang_code="ml").

## Runtime Compatibility

The published IndicXlit package uses legacy Fairseq components. PyTorch checkpoint loading is run with TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 as a runtime compatibility setting. Model weights are not modified.

## Dataset

The validation data is manually authored for this project to represent realistic Roman Malayalam and WhatsApp-style usage. It is not presented as a copied external benchmark or test set.

Categories include short chat, normal conversational Roman Malayalam, informal/chat expressions, spelling variation, mixed Malayalam-English chat, questions, requests, social/chat expressions, and longer messages.

## Metrics

Exact Match compares the generated Malayalam string with the project ground truth after trimming surrounding whitespace.

Normalized Character Similarity uses Python SequenceMatcher after normalizing surrounding and repeated whitespace.

Exact match alone is insufficient because Roman Malayalam has multiple possible spellings and transliteration systems can produce different but understandable Malayalam surface forms.

## Evaluation Status

The 12-sample seed was used for pipeline verification. The 50-sample dataset is an exploratory product-oriented validation set and is not yet treated as the final Phase 6 benchmark.

## Product Observation

Early testing indicates strong character-level similarity on many conversational and mixed messages, with weaker exact surface-form agreement on short informal expressions and spelling-sensitive chat input.

## Runtime

Set `TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1` when running the wrapper with the current PyTorch/Fairseq compatibility stack.
