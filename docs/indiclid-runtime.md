# IndicLID runtime setup

This document covers the optional AI4Bharat IndicLID runtime used by
the Malayalam WhatsApp Translator backend.

## Runtime requirements

Use a Python environment compatible with the upstream IndicLID model.
The model was smoke-tested in Google Colab with Python 3.11.13,
PyTorch 2.6.0, Transformers 4.53.2, and fasttext-wheel 0.9.2.

Install the IndicLID dependencies in a separate model environment.
Do not add heavy model dependencies to the lightweight backend CI
environment solely to run unit tests.

## Upstream source and model files

Clone the official IndicLID repository outside this project's Git
working tree and check out the revision used in the Phase 8 notebook:

    git clone https://github.com/AI4Bharat/IndicLID.git /content/IndicLID
    git -C /content/IndicLID switch --detach e4bfe42923c5ad581ccb64ca9feb38c0cd572ba8

Download the v1.0 FTN, FTR, and BERT model archives from the official
AI4Bharat IndicLID GitHub releases. Verify each archive before
extracting it into:

    /content/IndicLID/Inference/ai4bharat/models/

The runtime requires these exact files:

    IndicLID.py
    models/indiclid-ftn/model_baseline_roman.bin
    models/indiclid-ftr/model_baseline_roman.bin
    models/indiclid-bert/basline_nn_simple.pt

The spelling `basline_nn_simple.pt` comes from the upstream release.

Model archives and extracted weights must remain outside this
project's Git repository. Only load checkpoints from a source you trust;
the upstream loader uses PyTorch checkpoint deserialization.

## Connect the FastAPI backend

Set INDICLID_INFERENCE_DIR to the directory containing IndicLID.py
before starting the backend. For example, in Colab:

    export INDICLID_INFERENCE_DIR=/content/IndicLID/Inference/ai4bharat

The model loads lazily on the first translation request that needs
IndicLID and is cached for subsequent requests.

If INDICLID_INFERENCE_DIR is unset, the backend retains its existing
rule-based routing fallback. If the variable is set but the runtime
cannot initialize, /translate returns HTTP 503.

## Validation status

FTN, FTR, and the legacy BERT fallback were smoke-tested directly
in Colab. The backend adapter, routing, and error-handling unit tests
also passed using fake models.

A successful real-model /translate API test has not yet been recorded.
Do not treat the earlier direct-model tests as proof of complete
end-to-end API functionality.
