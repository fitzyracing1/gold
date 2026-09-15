#!/usr/bin/env python3
"""One-command demo: metric + gold snapshot + utterance valuation."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

from analogue_valuation_engine import AnalogueValuationEngine  # noqa: E402
from computing_metric import METRIC_EQ, is_metric_satisfied  # noqa: E402

SNAPSHOT = json.loads((ROOT / "snapshot.json").read_text())
UTTERANCE = SNAPSHOT["utterance"]


def main() -> None:
    engine = AnalogueValuationEngine()
    result = engine.valuate(UTTERANCE)
    v = result["valuation"]
    print("=" * 64)
    print("Analogue Valuation — gold snapshot demo")
    print(f"Metric: {METRIC_EQ}")
    print("=" * 64)
    print(f"c_gold     ${SNAPSHOT['c_gold_usd_per_oz']:,} / oz")
    print(f"c_light    {SNAPSHOT['c_light_m_s']} m/s")
    print(f"fastest    {SNAPSHOT['fastest_step_s']} s")
    print(f"step gold  {SNAPSHOT['step_priced_as_oz']} oz")
    print("-" * 64)
    print(f"USD VALUE  ${v['usd_value']:,.2f}")
    print(f"x={v['x']}  c={v['c']}  d={v['d']}")
    print(f"2xc-d      {v['metric_check']}")
    print(f"satisfied  {is_metric_satisfied(result['metric']['x'], result['metric']['c'], result['metric']['d'])}")
    print("=" * 64)


if __name__ == "__main__":
    main()
