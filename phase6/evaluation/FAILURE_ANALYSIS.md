# Phase 6 — IndicXlit Failure Analysis

## Validation Set

The analysis is based on the 75-sample manually authored project validation set.

- Total samples: 75
- Exact-match rate: 29.33%
- Mean normalized character similarity: 91.43%
- Median normalized character similarity: 94.74%
- Samples with similarity >= 0.90: 53/75
- Samples with similarity < 0.90: 22/75

## Failure Categories

### 1. Short Informal / Colloquial Expressions

Short messages are sensitive to small phonetic and orthographic differences.

Examples:

- `shari` → `ഷാരി` instead of `ശരി`
- `shari chetta` → `ഷാരി ചെറ്റ` instead of `ശരി ചേട്ടാ`
- `enthanu?` → `എന്തന്?` instead of `എന്താണ്?`

Observed category performance:

- Short chat mean similarity: 82.88%
- Chat expression mean similarity: 81.19%

### 2. Roman-Spelling Sensitivity

Different Roman spellings can produce different Malayalam outputs.

Examples:

- `nale` → `നാലെ`
- `naale` → `നാളെ`
- `evideya` → `എവിടെയ`
- `evideyaa` → `എവിടെയാ`

This shows that repeated vowels and conversational spelling conventions can materially affect transliteration.

### 3. Orthographic / Surface-Form Differences

Some outputs are close to the ground truth but differ in spelling or grammatical surface form.

Examples:

- `innu` → `ഇന്നു` versus `ഇന്ന്`
- `cheyyu` → `ചെയ്യു` versus `ചെയ്യൂ`
- `vilikkam` → `വിളിക്കം` versus `വിളിക്കാം`

These cases may remain understandable even when exact string matching fails.

### 4. Segmentation and Hyphenation

IndicXlit can preserve or introduce segmentation that differs from the expected Malayalam surface form.

Example:

- `college-il` → `കോളേജ്-ഇൽ`
- Ground truth: `കോളേജിൽ`

### 5. English / Abbreviation Handling

English fragments and abbreviations inside Malayalam-oriented chat can be difficult.

Examples:

- `pls vegam vaa` → `പിഎൽഎസ് വേഗം വാ`
- `oru msg ayakku` → `ഒരു എംഎസ്ജി അയക്കു`
- `okay alle?` → `ഒകയ് അല്ലെ?`

These outputs show that English abbreviations may be transliterated literally rather than mapped to a project-preferred conversational Malayalam representation.

### 6. Slang and Social Expressions

Informal slang can be substantially harder than standard conversational Malayalam.

Example:

- `pwoli macha` → `പ്വോളി മച്ച`

The output is less faithful to the expected Malayalam expression.

## Overall Observation

The main limitation observed in this validation is not failure to generate Malayalam script. IndicXlit generally produces Malayalam-script output, and many outputs have high character-level similarity.

The main weakness is preservation of the expected conversational Malayalam surface form for short informal expressions, slang, spelling-sensitive inputs, and English abbreviations.

Therefore, final product suitability should consider both quantitative similarity and qualitative usefulness rather than exact-match rate alone.

## Tuning Policy

No model weights, beam width, rescore setting, or candidate_v1 router behavior were changed after observing these validation results.

The failures are retained as validation findings.
