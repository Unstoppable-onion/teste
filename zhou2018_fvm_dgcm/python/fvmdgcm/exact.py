"""Exact (analytical) solution of Case 0: frictionless horizontal
reservoir-pipe-valve system, instantaneous valve closure at t = 0, no
cavitation (minimum head Hr - aV0/g > vapour head).

At the valve the head is a square wave of period 4L/a (Joukowsky):
    H(L,t) = Hr + aV0/g   for  (4k)   L/a < t < (4k+2) L/a
    H(L,t) = Hr - aV0/g   for  (4k+2) L/a < t < (4k+4) L/a
"""
from __future__ import annotations

import numpy as np

from .params import Case


def valve_head_exact(case: Case, t) -> np.ndarray:
    t = np.asarray(t, dtype=float)
    dH = case.a * case.V0 / case.fluid.g
    T2 = 2.0 * case.L / case.a
    phase = np.floor(t / T2).astype(int) % 2
    return np.where(phase == 0, case.Hr + dH, case.Hr - dH)
