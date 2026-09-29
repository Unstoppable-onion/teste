"""Boundary conditions coupled with the Riemann invariants (paper p. 3:
"U_1/2 and U_N+1/2 are obtained by coupling the Riemann invariant with a
head-flow boundary relation at time n").

Upstream reservoir (x = 0), C- invariant from cell I_1:
    H_B = Hr,   V_B = V_1 + (g/a)(Hr - H_1)
Downstream valve (x = L), C+ invariant from cell I_N:
    H_B = H_N + (a/g)(V_N - V_B),
    orifice law V_B = V_ref * tau * sqrt((H_B - H_down) / dH0)       [DED]
    tau(t) = max(0, 1 - t/Tc)  ("linear closure", paper p. 7)
"""
from __future__ import annotations

import math


def valve_tau(t: float, Tc: float) -> float:
    """Relative valve opening for a linear closure in Tc (instantaneous if Tc=0)."""
    if Tc <= 0.0:
        return 0.0
    return max(0.0, 1.0 - t / Tc)


def reservoir_state(H1: float, V1: float, Hr: float, a: float, g: float):
    return Hr, V1 + (g / a) * (Hr - H1)


def valve_velocity(Cp: float, tau: float, Vref: float, H_down: float, dH0: float,
                   B: float) -> float:
    """Solve V = Vref tau sqrt((Cp - B V - H_down)/dH0) with the compatibility
    relation H = Cp - B V (B = a/g for velocities).  Reverse flow through the
    valve is allowed (sign-symmetric orifice law)."""
    if tau <= 0.0 or Vref == 0.0:
        return 0.0
    Cv2 = (Vref * tau) ** 2 / dH0
    dh = Cp - H_down
    if dh >= 0.0:
        # V^2 + Cv2 B V - Cv2 dh = 0, positive root (cancellation-free form)
        return 2.0 * Cv2 * dh / (Cv2 * B + math.sqrt((Cv2 * B) ** 2 + 4.0 * Cv2 * dh))
    # reverse flow: V < 0, -V^2 = Cv2 (dh - B V)  ->  V^2 - Cv2 B V + Cv2 dh = 0
    return 2.0 * Cv2 * dh / (Cv2 * B + math.sqrt((Cv2 * B) ** 2 - 4.0 * Cv2 * dh))


def valve_state(HN: float, VN: float, tau: float, Vref: float, H_down: float,
                dH0: float, a: float, g: float):
    B = a / g
    Cp = HN + B * VN
    VB = valve_velocity(Cp, tau, Vref, H_down, dH0, B)
    return Cp - B * VB, VB
