"""ETA estimation from observed step durations.

ETA ≈ remaining_steps × smoothed_recent_step_time. The smoothing is an exponential moving average over the
step durations observed in the current run. When fewer than two durations exist, a per-workstation history
keyed by model/resolution/steps/frames may supply a mean step time; the basis is reported so the UI can say
which one it is. No estimate is produced without either source.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

EMA_ALPHA = 0.35
MIN_OBSERVED_DURATIONS = 2


@dataclass
class StepObservation:
    step: int
    at: datetime


def step_durations(observations: Sequence[StepObservation]) -> list[float]:
    """Seconds between consecutive step observations within one item (step must increase)."""
    durations: list[float] = []
    for prev, cur in zip(observations, observations[1:]):
        if cur.step > prev.step:
            delta = (cur.at - prev.at).total_seconds()
            if delta > 0:
                durations.append(delta / (cur.step - prev.step))
    return durations


def smoothed_step_seconds(durations: Sequence[float], alpha: float = EMA_ALPHA) -> float | None:
    if not durations:
        return None
    value = durations[0]
    for d in durations[1:]:
        value = alpha * d + (1 - alpha) * value
    return value


def timing_key(model: str | None, resolution: str | None, steps: int | None, frames: int | None, batch_size: int | None = None) -> str:
    """Per-workstation timing bucket. batch_size matters for image runs (WanGP denoises the batch together)."""
    parts = [model, resolution, steps, frames]
    if batch_size and batch_size > 1:
        parts.append(f"b{batch_size}")
    return "|".join(str(part or "") for part in parts)


def estimate(
    durations: Sequence[float],
    remaining_steps: int,
    history_mean: float | None = None,
) -> tuple[float | None, str | None]:
    """Return (eta_seconds, basis). basis is `recent_steps`, `history`, or None."""
    if remaining_steps <= 0:
        return 0.0, "recent_steps" if len(durations) >= MIN_OBSERVED_DURATIONS else ("history" if history_mean else None)
    if len(durations) >= MIN_OBSERVED_DURATIONS:
        per_step = smoothed_step_seconds(durations)
        if per_step:
            return round(remaining_steps * per_step, 1), "recent_steps"
    if history_mean and history_mean > 0:
        return round(remaining_steps * history_mean, 1), "history"
    return None, None
