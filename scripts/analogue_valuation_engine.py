#!/usr/bin/env python3
"""
analogue_valuation_engine.py
============================
Analogue Monetary Valuation Engine

Determines monetary (USD) value from speech-to-text input
while obeying the foundational sandbox metric:

    2 * x * c - d = 1

Pipeline:
    speech audio  →  STT (any engine)  →  text  →  this module  →  valuation

This program is built on the SandboxProgram template so the metric
is always present and enforced.
"""

from __future__ import annotations

import re
import math
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Ensure the scripts directory is on the path so the metric module resolves
_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from computing_metric import (
    SandboxProgram,
    MetricState,
    solve_d,
    is_metric_satisfied,
    METRIC_EQ,
)


# ---------------------------------------------------------------------------
# Feature extraction from speech-to-text
# ---------------------------------------------------------------------------

def extract_features(text: str) -> Dict[str, float]:
    """
    Turn raw STT text into continuous analogue features.
    All features are real-valued and intended for the metric.
    """
    if not text or not text.strip():
        return {
            "intensity": 0.1,
            "coherence": 0.1,
            "density": 0.1,
            "numeric_mass": 0.0,
            "word_count": 0.0,
            "char_count": 0.0,
        }

    cleaned = text.strip().lower()
    words = re.findall(r"\b[\w']+\b", cleaned)
    word_count = float(len(words))
    char_count = float(len(cleaned))

    # Intensity: length + emphasis signals (exclamation, caps in original, repeated letters)
    emphasis = len(re.findall(r"[!]{1,}", text)) + len(re.findall(r"[A-Z]{2,}", text))
    intensity = math.log1p(char_count) + 0.4 * emphasis
    intensity = max(0.15, min(intensity, 12.0))          # clamp to analogue range

    # Coherence: unique-word ratio (vocabulary richness) + sentence structure
    unique = len(set(words)) if words else 1
    vocab_ratio = unique / max(word_count, 1.0)
    sentence_count = max(1.0, len(re.findall(r"[.!?]+", text)))
    coherence = 0.55 * vocab_ratio + 0.45 * (1.0 / math.sqrt(sentence_count))
    coherence = max(0.12, min(coherence * 3.5, 8.0))

    # Density: characters per word (information packing)
    density = char_count / max(word_count, 1.0)
    density = max(0.5, min(density / 4.0, 4.0))

    # Numeric mass: any numbers spoken (quantities, prices, scores…)
    numbers = re.findall(r"[-+]?\d*\.?\d+", text)
    numeric_mass = sum(abs(float(n)) for n in numbers) if numbers else 0.0
    numeric_mass = math.log1p(numeric_mass)

    return {
        "intensity": intensity,
        "coherence": coherence,
        "density": density,
        "numeric_mass": numeric_mass,
        "word_count": word_count,
        "char_count": char_count,
    }


def features_to_metric(features: Dict[str, float]) -> Dict[str, float]:
    """
    Map analogue features onto the three metric variables.
    x  ← intensity + numeric influence   (magnitude / force of the speech)
    c  ← coherence * density             (clarity & information quality)
    d  is solved by the metric itself so 2xc - d = 1 always holds.
    """
    # Keep magnitudes modest so the later valuation stays in a useful range
    x = 0.35 * features["intensity"] + 0.15 * features["numeric_mass"]
    x = max(0.15, min(x, 4.5))

    c = 0.55 * features["coherence"] * (0.65 + 0.35 * features["density"])
    c = max(0.12, min(c, 3.8))

    d = solve_d(x, c)
    return {"x": x, "c": c, "d": d}


# ---------------------------------------------------------------------------
# Valuation
# ---------------------------------------------------------------------------

def compute_valuation(metric: MetricState, features: Dict[str, float]) -> Dict[str, float]:
    """
    Produce a monetary (USD) valuation from the metric state + features.

    The continuous analogue core is mapped into a dollar estimate while
    the metric 2xc - d = 1 remains strictly enforced.
    """
    # Core analogue signal from the metric triple
    core = (metric.x * metric.c) + (0.22 * metric.d)

    # Map core into a positive monetary base (continuous, non-linear)
    # Base grows with intensity/coherence; numeric content in speech adds directly.
    base = math.expm1(max(0.0, core) / 2.8) * 850.0          # soft exponential
    numeric_boost = features.get("numeric_mass", 0.0) * 420.0
    usd = max(0.0, base + numeric_boost)

    # Confidence / reliability of the STT-derived reading
    confidence = min(1.0, (features["word_count"] / 14.0) * (features["coherence"] / 2.8))
    confidence = max(0.05, confidence)

    return {
        "usd_value": round(usd, 2),
        "currency": "USD",
        "core": round(core, 4),
        "confidence": round(confidence, 4),
        "x": round(metric.x, 4),
        "c": round(metric.c, 4),
        "d": round(metric.d, 4),
        "metric_check": round(2 * metric.x * metric.c - metric.d, 6),
    }


# ---------------------------------------------------------------------------
# Engine (inherits the sandbox template)
# ---------------------------------------------------------------------------

class AnalogueValuationEngine(SandboxProgram):
    """
    Monetary (USD) valuation engine driven by speech-to-text.

    Converts spoken language / STT text into a continuous dollar estimate
    while strictly obeying the metric 2 * x * c - d = 1.

    Usage:
        engine = AnalogueValuationEngine()
        result = engine.valuate("the spoken words after STT")
        # result["valuation"]["usd_value"]  →  monetary estimate in USD
    """

    def __init__(self, name: str = "analogue_valuation_engine"):
        super().__init__(x=1.0, c=1.0, name=name)
        self.last_features: Dict[str, float] = {}
        self.last_valuation: Dict[str, float] = {}

    def valuate(self, text: str) -> Dict[str, Any]:
        """
        Main public method.
        Accepts the text produced by any speech-to-text system.
        Returns a full valuation record while keeping the metric invariant.
        """
        features = extract_features(text)
        metric_vars = features_to_metric(features)

        # Update the living metric state (d is auto-consistent)
        self.set_metric(x=metric_vars["x"], c=metric_vars["c"])

        valuation = compute_valuation(self.metric, features)

        self.last_features = features
        self.last_valuation = valuation

        return {
            "input_text": text,
            "features": {k: round(v, 4) for k, v in features.items()},
            "metric": self.metric.as_dict(),
            "valuation": valuation,
            "equation": METRIC_EQ,
            "satisfied": is_metric_satisfied(
                self.metric.x, self.metric.c, self.metric.d
            ),
        }

    def _execute(self, text: str = "", **kwargs) -> Dict[str, Any]:
        """Required by SandboxProgram template."""
        return self.valuate(text)

    def status(self) -> Dict[str, Any]:
        base = super().status()
        base["last_value"] = self.last_valuation.get("value")
        base["last_confidence"] = self.last_valuation.get("confidence")
        return base


# ---------------------------------------------------------------------------
# Demo / CLI
# ---------------------------------------------------------------------------

DEMO_UTTERANCES = [
    "The package is ready and valued at forty two thousand.",
    "I need this done immediately, high priority, no delays!",
    "maybe later we can look at it again",
    "Revenue came in at 1.8 million with strong margins and clear growth.",
    "",  # empty / silence
]


if __name__ == "__main__":
    print("=" * 64)
    print("Analogue Monetary Valuation Engine")
    print(f"Metric foundation: {METRIC_EQ}")
    print("Input: speech-to-text  →  monetary (USD) value")
    print("=" * 64)

    engine = AnalogueValuationEngine()

    for i, utterance in enumerate(DEMO_UTTERANCES, 1):
        print(f"\n--- Utterance {i} ---")
        print(f"STT text: {utterance!r}")
        result = engine.run(text=utterance)
        v = result["valuation"]
        print(f"  features   intensity={result['features']['intensity']:.3f}  "
              f"coherence={result['features']['coherence']:.3f}")
        print(f"  metric     x={v['x']:.4f}  c={v['c']:.4f}  d={v['d']:.4f}")
        print(f"  USD VALUE  ${v['usd_value']:,.2f}   (confidence {v['confidence']:.2f})")
        print(f"  check      2xc - d = {v['metric_check']:.6f}")

    print("\n" + "=" * 64)
    print("Engine ready. Pass any STT text → engine.valuate(text) → USD estimate")
    print("=" * 64)
