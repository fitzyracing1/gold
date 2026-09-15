---
name: analogue-valuation-engine
description: Activate for monetary (USD) valuation from speech-to-text using the sandbox metric 2xc-d=1. Use when converting spoken language or STT text into dollar estimates, building monetary valuation engines on the computing metric, or when the user mentions monetary valuation, speech-to-money, STT dollar value, analogue monetary evaluation, or 2xc-d valuation. Triggers include analogue valuation engine, monetary evaluation, speech to text value, STT valuation, dollar estimate from speech, metric-based valuation.
---

# Analogue Valuation Engine

## Overview

Turns speech-to-text into a continuous monetary (USD) valuation while strictly obeying the foundational sandbox metric:

```
2 * x * c - d = 1
```

The engine is built on `SandboxProgram` so the metric is always present and enforced.

## Core Pipeline

```
speech audio → any STT system → text
                             → extract analogue features (intensity, coherence, density, numeric mass)
                             → map features onto metric variables x, c
                             → solve d so 2xc - d = 1
                             → compute continuous USD monetary estimate
```

## How to Use

1. Import and instantiate:

```python
from scripts.analogue_valuation_engine import AnalogueValuationEngine

engine = AnalogueValuationEngine()
```

2. Pass the text produced by any speech-to-text engine:

```python
result = engine.valuate("Revenue came in at 1.8 million with strong growth.")
# or
result = engine.run(text="the spoken words after STT")
```

3. Read the output:

- `result["valuation"]["usd_value"]` — monetary estimate in USD
- `result["valuation"]["confidence"]` — reliability of the STT-derived reading
- `result["metric"]` — current `{x, c, d}` that satisfy the metric
- `result["satisfied"]` — always True when the engine is functioning correctly
- `result["features"]` — the intermediate analogue features extracted from the text

## Metric Invariant (never violate)

Every valuation must keep:

```
2 * x * c - d == 1
```

- `x` is driven by intensity + numeric content of the speech
- `c` is driven by coherence and information density
- `d` is always solved from x and c (never set independently when valuating)

Use the helpers in `scripts/computing_metric.py` (`solve_d`, `is_metric_satisfied`, `MetricState`, `SandboxProgram`) for any extension.

## Feature Mapping

| Feature | Source | Role |
|---------|--------|------|
| intensity | length + emphasis (caps, !) | magnitude / force → x |
| coherence | vocab richness + sentence structure | clarity → c |
| density | chars per word | information packing → c |
| numeric_mass | spoken numbers / quantities | boosts x |

## Extension Points

- Adjust feature scaling inside `extract_features` or `features_to_metric` for domain-specific ranges.
- Replace the valuation function (`compute_valuation`) while keeping the metric intact.
- Subclass `AnalogueValuationEngine` (itself a `SandboxProgram`) for specialized valuation domains.
- Wire a real STT backend (Whisper, on-device, cloud) in front of `.valuate(text)`.

## Files

- `scripts/computing_metric.py` — foundational metric + `SandboxProgram` base class
- `scripts/analogue_valuation_engine.py` — the valuation engine itself

## Quick Test

```bash
python3 scripts/analogue_valuation_engine.py
```

This runs the built-in demo utterances and prints value + metric for each.
