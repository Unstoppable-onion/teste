"""Godunov-type finite-volume operators for the linear water-hammer system.

Governing equations (paper Eq. 4), convective terms neglected:
    dU/dt + d f(U)/dx = s(U),   U = (H, V),   f(U) = A U,
    A = [[0, a^2/g], [g, 0]],   s(U) = (0, -f V|V| / (2 D)).

Exact Riemann solution (paper Eq. 6) at an interface with left/right states
U_L, U_R:
    H* = (H_L + H_R)/2 + (a/2g)(V_L - V_R)
    V* = (V_L + V_R)/2 + (g/2a)(H_L - H_R)
    flux = A U* = (a^2/g V*, g H*).
"""
from __future__ import annotations

import numpy as np


def riemann_state(HL, VL, HR, VR, a, g):
    """Interface state U* of the exact Riemann solution (paper Eq. 6)."""
    Hs = 0.5 * (HL + HR) + 0.5 * (a / g) * (VL - VR)
    Vs = 0.5 * (VL + VR) + 0.5 * (g / a) * (HL - HR)
    return Hs, Vs


def minmod(d1, d2):
    """MINMOD limiter (componentwise)."""
    return np.where(d1 * d2 > 0.0, np.sign(d1) * np.minimum(np.abs(d1), np.abs(d2)), 0.0)


def interface_states(H, V, a, g, lam, order):
    """Left/right states at the N+1 interfaces of the extended array.

    ``H``/``V`` include two virtual cells on each side (length N+4):
    index 0,1 = I_-1, I_0 ; 2..N+1 = I_1..I_N ; N+2, N+3 = I_N+1, I_N+2.
    ``lam`` = dt/dx.  Returns (HL, VL, HR, VR) for interfaces 1/2 .. N+1/2
    (length N+1).

    order 1: piecewise constant (Godunov).
    order 2: MUSCL-Hancock (Toro 2009, Sec. 14.4) with MINMOD slopes; the
             boundary-extrapolated values are evolved by dt/2 with the
             homogeneous (source-free) flux, the source being handled by
             time splitting (paper Eqs. 7-9).
    """
    if order == 1:
        return H[1:-2], V[1:-2], H[2:-1], V[2:-1]
    # slopes for cells 1..N+2 (extended index), i.e. I_0 .. I_N+1
    dH = minmod(H[1:-1] - H[:-2], H[2:] - H[1:-1])
    dV = minmod(V[1:-1] - V[:-2], V[2:] - V[1:-1])
    Hc, Vc = H[1:-1], V[1:-1]
    # half-step evolution: U -> U - (lam/2) A dU   (f(U_L) - f(U_R) = -A dU)
    cH = 0.5 * lam * (a * a / g) * dV
    cV = 0.5 * lam * g * dH
    HmL = Hc - 0.5 * dH - cH   # evolved left boundary value of each cell
    VmL = Vc - 0.5 * dV - cV
    HmR = Hc + 0.5 * dH - cH   # evolved right boundary value of each cell
    VmR = Vc + 0.5 * dV - cV
    # interface k+1/2 between cells (I_k, I_k+1), k = 0..N
    return HmR[:-1], VmR[:-1], HmL[1:], VmL[1:]


def friction_source_rk2(V, dt, f, D):
    """Source step, paper Eqs. (8)-(9): explicit 2nd-order Runge-Kutta
    (midpoint) for dV/dt = -f V|V|/(2D); H is unaffected."""
    if f == 0.0:
        return V
    k = f / (2.0 * D)
    Vh = V - 0.5 * dt * k * V * np.abs(V)
    return V - dt * k * Vh * np.abs(Vh)
