# Analogue Valuation Engine — Gold Snapshot

Treat this as gold.

Sandbox metric (never violate):

```
2 * x * c - d = 1
```

Spoken / written form used in this session:

```
2 c d - 1 c = f(x)
```

which factors as `c (2d - 1) = f(x)`. Dual reading of `c`:

- `c_gold` ≈ current USD per troy ounce
- `c_light` = 299792458 m/s

## Snapshot — 2026-09-15

| Item | Value |
|---|---|
| Gold (spot-ish, 15 Sep 2026) | ~$4,294 / troy oz |
| Utterance valuation (engine) | $4,557.88 USD |
| Metric state | x ≈ 2.1067, c ≈ 1.6753, d ≈ 6.0585 |
| Metric check `2xc - d` | 1.000000 |
| Fastest in-process step | ≈ 4.01e-7 s (401 ns) |
| Process spawn (`true`) | ≈ 3 ms (not a single step) |
| One fastest step priced as | 1 oz Au ≈ $4,294 |
| Implied rate | ≈ $1.07e10 / second |

## Files

- `scripts/computing_metric.py` — `2xc - d = 1` helpers + `SandboxProgram`
- `scripts/analogue_valuation_engine.py` — STT text → USD while the metric holds
- `SKILL.md` — skill contract
- `snapshot.json` — numbers from this session
- `run_demo.py` — one-command demo

## Run

```bash
python3 run_demo.py
python3 scripts/analogue_valuation_engine.py
```

## Push

This folder is the unit of work. Zip is `analogue-valuation-gold.zip`.

## Documentation

- In-repo docs: [docs/](docs/index.md)
- Wiki: [https://github.com/fitzyracing1/gold/wiki](https://github.com/fitzyracing1/gold/wiki)
