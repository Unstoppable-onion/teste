"""First/second-order FVM Godunov solver with discrete cavities (FVM-DGCM,
FVM-DVCM) for the reservoir-pipe-valve system of Zhou et al. (2018).

Time step (paper Eqs. 5-9 and Fig. 3):
  1. boundary states U_1/2, U_N+1/2 at time n (Riemann invariants + BC),
     copied into the virtual cells I_-1, I_0, I_N+1, I_N+2;
  2. interface states (Godunov or MUSCL-Hancock) and exact Riemann fluxes;
  3. pure wave propagation, Eq. (7);
  4. friction source by RK2 splitting, Eqs. (8)-(9);
  5. discrete cavity correction (DGCM Methods I/II or DVCM) per reach.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .boundaries import reservoir_state, valve_state, valve_tau
from .cavity import CavityState, apply_dgcm, apply_dvcm
from .godunov import friction_source_rk2, interface_states, riemann_state
from .params import Case, Numerics


@dataclass
class Result:
    t: np.ndarray            # output times, s
    H_valve: np.ndarray      # head at the valve (boundary state U_N+1/2), m
    H_cellN: np.ndarray      # head of the last cell I_N, m
    V_valve: np.ndarray      # velocity through the valve, m/s
    mass_error: np.ndarray   # liquid+cavity volume balance error, m^3
    Vg_total: np.ndarray     # total cavity volume, m^3
    meta: dict


def initial_state(case: Case, x: np.ndarray):
    """Steady state: uniform V0 and linear hydraulic grade line (entrance
    and velocity-head losses neglected)."""
    f = case.friction
    H = case.Hr - f * x * case.V0 ** 2 / (2.0 * case.fluid.g * case.D)
    V = np.full_like(x, case.V0)
    return H, V


def run_fvm(case: Case, num: Numerics, t_end: float | None = None,
            store_every: int = 1, record_profiles_at=(), initial=None) -> Result:
    """Simulate ``case`` with the options ``num``.

    ``initial``: optional callable x -> (H, V) replacing the steady initial
    state (used by the verification tests)."""
    fl = case.fluid
    g, a, D, A = fl.g, case.a, case.D, case.area
    f = case.friction
    Ns = num.Ns
    N = 2 * Ns
    dx = case.L / N
    dt = num.Cr * dx / a
    lam = dt / dx
    t_end = case.t_end if t_end is None else t_end
    nsteps = int(round(t_end / dt))

    xc = (np.arange(N) + 0.5) * dx
    Hc, Vc = initial_state(case, xc) if initial is None else initial(xc)
    Hc, Vc = np.array(Hc, dtype=float), np.array(Vc, dtype=float)

    # valve reference: discrete steady state of the first-order scheme
    # (interface velocity V0 + g*hf_cell/(2a), head H(L)); keeps the initial
    # steady state exactly stationary (see tests/test_steady_state.py)
    H_valve0 = case.Hr - f * case.L * case.V0 ** 2 / (2 * g * D)
    hf_cell = f * dx * case.V0 ** 2 / (2 * g * D)
    Vref = case.V0 + g * hf_cell / (2 * a)
    dH0 = case.dH_valve0
    H_down = H_valve0 - dH0

    # cavities at the middle of each reach
    zc = case.z((2 * np.arange(Ns) + 1) * dx)
    vol_reach = A * 2 * dx
    C3 = fl.H0_std * num.alpha0 * vol_reach if num.model == "DGCM" else 0.0
    cav = CavityState(Ns, zc, fl.Hv, C3)
    cav.limit_growth = num.limit_gas_growth
    cav.fallback = num.fallback
    if num.model == "DGCM":
        cav.init_equilibrium(Hc)

    # extended arrays with two virtual cells at each end
    H = np.empty(N + 4)
    V = np.empty(N + 4)
    H[2:-2], V[2:-2] = Hc, Vc

    nout = nsteps // store_every + 1
    t_out = np.empty(nout)
    Hv_out = np.empty(nout)
    HN_out = np.empty(nout)
    Vv_out = np.empty(nout)
    merr = np.empty(nout)
    vg_out = np.empty(nout)
    profiles = {}

    # liquid storage (compressibility) coefficient: dVol = gA/a^2 dH dx
    kst = g * A / a ** 2
    mass0 = kst * dx * Hc.sum() + cav.Vg.sum()
    net_in = 0.0

    def boundary(t):
        HB0, VB0 = reservoir_state(H[2], V[2], case.Hr, a, g)
        tau = valve_tau(t, case.Tc)
        HBN, VBN = valve_state(H[-3], V[-3], tau, Vref, H_down, dH0, a, g)
        return HB0, VB0, HBN, VBN

    k = 0
    for n in range(nsteps + 1):
        t = n * dt
        HB0, VB0, HBN, VBN = boundary(t)
        if n % store_every == 0:
            t_out[k], Hv_out[k], HN_out[k], Vv_out[k] = t, HBN, H[-3], VBN
            merr[k] = kst * dx * H[2:-2].sum() + cav.Vg.sum() - mass0 - net_in
            vg_out[k] = cav.Vg.sum()
            k += 1
        for tp in record_profiles_at:
            if abs(t - tp) < 0.5 * dt:
                profiles[tp] = (xc.copy(), H[2:-2].copy(), V[2:-2].copy(), cav.Vg.copy())
        if n == nsteps:
            break
        H[0] = H[1] = HB0
        V[0] = V[1] = VB0
        H[-1] = H[-2] = HBN
        V[-1] = V[-2] = VBN
        HL, VL, HR, VR = interface_states(H, V, a, g, lam, num.order)
        Hs, Vs = riemann_state(HL, VL, HR, VR, a, g)
        # Eq. (7): pure wave propagation
        Hn = H[2:-2] - lam * (a * a / g) * (Vs[1:] - Vs[:-1])
        Vn = V[2:-2] - lam * g * (Hs[1:] - Hs[:-1])
        # Eqs. (8)-(9): friction source
        Vn = friction_source_rk2(Vn, dt, f, D)
        # boundary volume fluxes (liquid mass balance diagnostic)
        net_in += (Vs[0] - Vs[-1]) * A * dt
        # discrete cavities
        Qn = Vn * A
        if num.model == "DGCM":
            apply_dgcm(cav, Hn, Qn, dt, num.C_ap, num.collapse)
        elif num.model == "DVCM":
            apply_dvcm(cav, Hn, Qn, dt)
        elif num.model != "none":
            raise ValueError(num.model)
        H[2:-2], V[2:-2] = Hn, Vn

    meta = dict(case=case.name, Ns=Ns, N=N, dx=dx, dt=dt, Cr=num.Cr, C_ap=num.C_ap,
                alpha0=num.alpha0, order=num.order, model=num.model, collapse=num.collapse,
                limit_gas_growth=num.limit_gas_growth,
                f=f, Hv=fl.Hv, z_valve=case.z(case.L), H_valve0=H_valve0,
                n_fallback=cav.n_fallback, profiles=profiles)
    return Result(t_out[:k], Hv_out[:k], HN_out[:k], Vv_out[:k], merr[:k], vg_out[:k], meta)
