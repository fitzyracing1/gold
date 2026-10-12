# Analogue Valuation Engine: Gold Snapshot (repo: gold)

This is a sandbox experiment built around the metric `2 * x * c - d = 1`. It turns speech-to-text utterances into a USD valuation while the metric holds, and it records a snapshot of values from 2026-09-15 in `snapshot.json` and the README. The README's figures are session numbers, not market data feeds.

## Getting started

```bash
python3 run_demo.py
python3 scripts/analogue_valuation_engine.py
```

## Files

| Path | Role |
|---|---|
| `scripts/computing_metric.py` | `2xc - d = 1` helpers, `METRIC_EQ`, `is_metric_satisfied`, `SandboxProgram` |
| `scripts/analogue_valuation_engine.py` | `AnalogueValuationEngine` (text → USD) |
| `run_demo.py` | one-command demo |
| `SKILL.md` | skill contract |
| `snapshot.json` | recorded session values |

The repo has no tests, no CI and no LICENSE file. Copyright (c) 2026 Joshua Almeida
