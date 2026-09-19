"""Certainty equivalents and risk premia for CRRA utility."""

from __future__ import annotations

import math


def crra_u(w: float, gamma: float) -> float:
    if w <= 0:
        raise ValueError("wealth must be positive")
    if abs(gamma - 1.0) < 1e-12:
        return math.log(w)
    return (w ** (1.0 - gamma) - 1.0) / (1.0 - gamma)


def crra_inv(u: float, gamma: float) -> float:
    if abs(gamma - 1.0) < 1e-12:
        return math.exp(u)
    return (u * (1.0 - gamma) + 1.0) ** (1.0 / (1.0 - gamma))


def certainty_equivalent(outcomes: list[float], probs: list[float], gamma: float) -> dict[str, float]:
    eu = sum(p * crra_u(w, gamma) for p, w in zip(probs, outcomes))
    ce = crra_inv(eu, gamma)
    ev = sum(p * w for p, w in zip(probs, outcomes))
    return {"expected_wealth": ev, "certainty_equivalent": ce, "risk_premium": ev - ce}


if __name__ == "__main__":
    # Fifty-fifty lottery between 4 and 16
    outcomes = [4.0, 16.0]
    probs = [0.5, 0.5]
    for gamma in [0.5, 1.0, 2.0, 3.0]:
        result = certainty_equivalent(outcomes, probs, gamma)
        print(f"gamma={gamma:.1f}  CE={result['certainty_equivalent']:.4f}  premium={result['risk_premium']:.4f}")
