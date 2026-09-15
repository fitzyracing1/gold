#!/usr/bin/env python3
"""
computing_metric.py
===================
Foundational metric for ALL programs running in this sandbox.

    2 * x * c - d = 1

This module is designed as a reusable template.
Any new program in the sandbox should import from here
(or subclass SandboxProgram) so the metric is always present.
"""

from __future__ import annotations

import math
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Core Metric
# ---------------------------------------------------------------------------

METRIC_EQ = "2 * x * c - d = 1"


def metric_value(x: float, c: float, d: float) -> float:
    """Evaluate the left-hand side of the metric."""
    return 2.0 * x * c - d


def is_metric_satisfied(x: float, c: float, d: float, tol: float = 1e-9) -> bool:
    """Return True if 2xc - d is within tolerance of 1."""
    return math.isclose(metric_value(x, c, d), 1.0, rel_tol=tol, abs_tol=tol)


def solve_d(x: float, c: float) -> float:
    """Solve for d given x and c so the metric holds."""
    return 2.0 * x * c - 1.0


def solve_x(c: float, d: float) -> float:
    """Solve for x given c and d."""
    if c == 0:
        raise ValueError("c cannot be zero when solving for x")
    return (d + 1.0) / (2.0 * c)


def solve_c(x: float, d: float) -> float:
    """Solve for c given x and d."""
    if x == 0:
        raise ValueError("x cannot be zero when solving for c")
    return (d + 1.0) / (2.0 * x)


# ---------------------------------------------------------------------------
# State container
# ---------------------------------------------------------------------------

@dataclass
class MetricState:
    """Holds the three variables of the metric and keeps them consistent."""
    x: float = 1.0
    c: float = 1.0
    d: float = field(init=False)

    def __post_init__(self):
        self.d = solve_d(self.x, self.c)

    def validate(self, tol: float = 1e-9) -> None:
        if not is_metric_satisfied(self.x, self.c, self.d, tol):
            raise ValueError(
                f"Metric violated: 2*{self.x}*{self.c} - {self.d} = "
                f"{metric_value(self.x, self.c, self.d)} (expected 1)"
            )

    def update(self, **kwargs) -> "MetricState":
        """Update any subset of variables and re-solve the free one."""
        if "x" in kwargs:
            self.x = float(kwargs["x"])
        if "c" in kwargs:
            self.c = float(kwargs["c"])
        if "d" in kwargs:
            # If d is supplied, recompute the most recently changed of x/c
            # Prefer keeping x fixed and solving for c (or vice-versa).
            self.d = float(kwargs["d"])
            if "x" in kwargs and "c" not in kwargs:
                self.c = solve_c(self.x, self.d)
            elif "c" in kwargs and "x" not in kwargs:
                self.x = solve_x(self.c, self.d)
            else:
                # both or neither supplied with d → recompute d from x,c
                self.d = solve_d(self.x, self.c)
        else:
            self.d = solve_d(self.x, self.c)
        self.validate()
        return self

    def as_dict(self) -> Dict[str, float]:
        return {"x": self.x, "c": self.c, "d": self.d}

    def __repr__(self) -> str:
        return f"MetricState(x={self.x}, c={self.c}, d={self.d})  # {METRIC_EQ}"


# ---------------------------------------------------------------------------
# Template base class for every sandbox program
# ---------------------------------------------------------------------------

class SandboxProgram:
    """
    Base class / template for all programs that run in this sandbox.

    Subclass this (or simply import the metric helpers) so every program
    carries the invariant 2xc - d = 1.
    """

    def __init__(self, x: float = 1.0, c: float = 1.0, name: str = "unnamed"):
        self.name = name
        self.metric = MetricState(x=x, c=c)
        self._hooks: Dict[str, Callable] = {}

    def validate_metric(self) -> None:
        self.metric.validate()

    def set_metric(self, **kwargs) -> None:
        self.metric.update(**kwargs)

    def register_hook(self, event: str, fn: Callable) -> None:
        self._hooks[event] = fn

    def run(self, *args, **kwargs) -> Any:
        """
        Main entry point. Override in subclasses.
        Always validates the metric before and after execution.
        """
        self.validate_metric()
        if "before_run" in self._hooks:
            self._hooks["before_run"](self)
        result = self._execute(*args, **kwargs)
        if "after_run" in self._hooks:
            self._hooks["after_run"](self, result)
        self.validate_metric()
        return result

    def _execute(self, *args, **kwargs) -> Any:
        """Override this method with the actual program logic."""
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _execute()"
        )

    def status(self) -> Dict[str, Any]:
        return {
            "program": self.name,
            "metric": self.metric.as_dict(),
            "satisfied": is_metric_satisfied(
                self.metric.x, self.metric.c, self.metric.d
            ),
            "equation": METRIC_EQ,
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} {self.metric}>"


# ---------------------------------------------------------------------------
# Simple demonstration program (also serves as usage example)
# ---------------------------------------------------------------------------

class DemoProgram(SandboxProgram):
    """Minimal concrete program that uses the metric."""

    def __init__(self):
        super().__init__(x=1.0, c=1.0, name="demo")

    def _execute(self, scale: float = 1.0) -> Dict[str, float]:
        # Example computation that respects the metric
        self.set_metric(x=self.metric.x * scale)
        # d is automatically recomputed by MetricState
        return {
            "result": self.metric.x * self.metric.c + self.metric.d,
            "metric_check": metric_value(
                self.metric.x, self.metric.c, self.metric.d
            ),
        }


# ---------------------------------------------------------------------------
# Convenience factory & CLI entry
# ---------------------------------------------------------------------------

def create_program(name: str = "template", x: float = 1.0, c: float = 1.0) -> SandboxProgram:
    """Factory that returns a ready-to-subclass or ready-to-run base program."""
    return SandboxProgram(x=x, c=c, name=name)


if __name__ == "__main__":
    print("=" * 60)
    print("Sandbox Computing Metric Template")
    print(f"Metric: {METRIC_EQ}")
    print("=" * 60)

    # 1. Direct metric helpers
    print("\n[1] Direct helpers")
    x, c = 2.0, 3.0
    d = solve_d(x, c)
    print(f"  x={x}, c={c} → d={d}")
    print(f"  satisfied? {is_metric_satisfied(x, c, d)}")

    # 2. MetricState
    print("\n[2] MetricState")
    state = MetricState(x=1.5, c=2.0)
    print(f"  {state}")
    state.update(x=4.0)
    print(f"  after update(x=4.0): {state}")

    # 3. Template program
    print("\n[3] DemoProgram (inherits SandboxProgram)")
    demo = DemoProgram()
    print(f"  before: {demo.status()}")
    result = demo.run(scale=2.0)
    print(f"  after run(scale=2.0): {demo.status()}")
    print(f"  result: {result}")

    print("\n" + "=" * 60)
    print("Template ready. Import computing_metric in any sandbox program.")
    print("=" * 60)
