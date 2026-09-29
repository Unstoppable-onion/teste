"""Classic MOC discrete gas cavity model on a staggered grid
(Wylie 1984; Wylie et al. 1993, "Fluid Transients in Systems", Ch. 8), used
by the paper as reference for Fig. 11.

Grid: Ns reaches, nodes i = 0..Ns, dx = L/Ns, dt = dx/a (Courant 1).
Staggered grid: at step k only the nodes with (i + k) even are computed from
the neighbours computed at step k-1, so each node is updated every 2 dt.

Compatibility equations (Q in m^3/s, B = a/(gA), R = f dx/(2 g D A^2)):
    C+ : H_P = C_P - B Q_Pu,   C_P = H_A + B Q_A - R Q_A|Q_A|   (A = node i-1, downstream-side Q)
    C- : H_P = C_M + B Q_P,    C_M = H_B - B Q_B + R Q_B|Q_B|   (B = node i+1, upstream-side Q_u)
Gas cavity at every interior node and at the valve (isothermal gas law):
    Vg_P (H_P - z - Hv) = C3 = p0 alpha0 Vol / (rho g)
    Vg_P = Vg_old + 2dt [psi (Q_P - Q_Pu) + (1 - psi)(Q - Q_u)_old]
which gives a quadratic in y = H_P - z - Hv (positive root).  psi = 1 by
default (fully implicit weighting, recommended by Bergant et al. 2006) [DED].
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .boundaries import valve_tau, valve_velocity
from .params import Case


@dataclass
class MocResult:
    t: np.ndarray
    H_valve: np.ndarray
    meta: dict


def _gas_root(K1: float, K0: float, C3: float) -> float:
    """Positive root y of K1 y^2 + K0 y - C3 = 0 (numerically stable)."""
    disc = math.sqrt(K0 * K0 + 4.0 * K1 * C3)
    if K0 >= 0.0:
        return 2.0 * C3 / (K0 + disc)
    return (-K0 + disc) / (2.0 * K1)


def run_moc_dgcm(case: Case, Ns: int = 32, alpha0: float = 1e-7, psi: float = 1.0,
                 t_end: float | None = None) -> MocResult:
    if Ns % 2:
        raise ValueError("staggered grid requires an even number of reaches")
    fl = case.fluid
    g, a, D, A = fl.g, case.a, case.D, case.area
    f = case.friction
    dx = case.L / Ns
    dt = dx / a
    t_end = case.t_end if t_end is None else t_end
    nsteps = int(round(t_end / dt))
    B = a / (g * A)
    R = f * dx / (2.0 * g * D * A * A)

    x = np.arange(Ns + 1) * dx
    zhv = case.z(x) + fl.Hv            # vapour piezometric head at nodes
    C3 = fl.H0_std * alpha0 * A * dx   # gas constant of each node (reach volume)
    Q0 = case.V0 * A
    H = case.Hr - f * x * case.V0 ** 2 / (2.0 * g * D)
    Q = np.full(Ns + 1, Q0)            # downstream-side discharge
    Qu = np.full(Ns + 1, Q0)           # upstream-side discharge
    Vg = C3 / (H - zhv)
    Vg[0] = 0.0                        # no cavity at the reservoir
    t_last = np.zeros(Ns + 1)          # time of the last update of each node

    # valve: orifice law, steady loss dH0 (same as FVM model)
    H_valve0 = H[-1]
    dH0 = case.dH_valve0
    H_down = H_valve0 - dH0

    t_out = [0.0]
    h_out = [H[-1]]
    for k in range(1, nsteps + 1):
        t = k * dt
        Hn, Qn, Qun = H.copy(), Q.copy(), Qu.copy()
        par = k % 2
        for i in range(par, Ns + 1, 2):
            dti = t - t_last[i]
            if i == 0:  # upstream reservoir
                CM = H[1] - B * Qu[1] + R * Qu[1] * abs(Qu[1])
                Hn[0] = case.Hr
                Qn[0] = Qun[0] = (case.Hr - CM) / B
                continue
            CP = H[i - 1] + B * Q[i - 1] - R * Q[i - 1] * abs(Q[i - 1])
            if i == Ns:  # valve with gas cavity
                tau = valve_tau(t, case.Tc)
                if tau > 0.0:
                    # valve moving: liquid solution (C+ with orifice law),
                    # gas volume in equilibrium with the (high) pressure
                    Qv = A * valve_velocity(CP, tau, case.V0, H_down, dH0, B * A)
                    Hn[i] = CP - B * Qv
                    Qn[i] = Qun[i] = Qv
                    Vg[i] = C3 / max(Hn[i] - zhv[i], 1e-12)
                else:
                    Qv = 0.0
                    K1 = psi * dti / B
                    K0 = Vg[i] + dti * (psi * (Qv - (CP - zhv[i]) / B)
                                        + (1.0 - psi) * (Q[i] - Qu[i]))
                    y = _gas_root(K1, K0, C3)
                    Hn[i] = y + zhv[i]
                    Vg[i] = C3 / y
                    Qn[i] = Qv
                    Qun[i] = (CP - Hn[i]) / B
            else:  # interior node with gas cavity
                CM = H[i + 1] - B * Qu[i + 1] + R * Qu[i + 1] * abs(Qu[i + 1])
                K1 = 2.0 * psi * dti / B
                K0 = Vg[i] + dti * (psi * (2.0 * zhv[i] - CP - CM) / B
                                    + (1.0 - psi) * (Q[i] - Qu[i]))
                y = _gas_root(K1, K0, C3)
                Hn[i] = y + zhv[i]
                Vg[i] = C3 / y
                Qn[i] = (Hn[i] - CM) / B
                Qun[i] = (CP - Hn[i]) / B
            t_last[i] = t
        H, Q, Qu = Hn, Qn, Qun
        if par == 0:  # valve node updated at even steps
            t_out.append(t)
            h_out.append(H[-1])
    return MocResult(np.array(t_out), np.array(h_out),
                     dict(case=case.name, Ns=Ns, dx=dx, dt=dt, psi=psi, alpha0=alpha0, f=f))
