"""Verification tests of the Python implementation (pytest).

They check, independently of the paper's figures:
  * exactness of the Godunov/MUSCL-Hancock schemes at Cr = 1 (linear system);
  * the analytical solution of Case 0 (C_-ap = 1);
  * preservation of the discrete steady state with friction;
  * liquid volume conservation without cavitation;
  * order of convergence on a smooth problem (1st and 2nd order);
  * the gas law / cavity relations (Eqs. 11, 15, 16);
  * the orifice valve law and the MOC-DGCM;
  * dimensional consistency (similarity and datum invariance).
"""
from __future__ import annotations

import math

import numpy as np
import pytest

from fvmdgcm.boundaries import valve_velocity
from fvmdgcm.cavity import CavityState, apply_dgcm, apply_dvcm
from fvmdgcm.exact import valve_head_exact
from fvmdgcm.fvm_solver import run_fvm
from fvmdgcm.godunov import minmod, riemann_state
from fvmdgcm.moc_dgcm import run_moc_dgcm
from fvmdgcm.params import CASES, Fluid, Numerics

C0 = CASES["case0"]
C1 = CASES["case1"]


def away_from_fronts(case, t, margin=0.02):
    T2 = 2 * case.L / case.a
    ph = (t / T2) % 1.0
    return (ph > margin) & (ph < 1 - margin) & (t > 0)


# ---------------------------------------------------------------- Riemann
def test_riemann_invariants():
    """U* satisfies the jump conditions: the left-going wave carries
    H + (a/g)V from the left state, the right-going one H - (a/g)V from the
    right state (paper Eq. 6)."""
    a, g = 1280.0, 9.81
    HL, VL, HR, VR = 30.0, 0.3, 10.0, -0.1
    Hs, Vs = riemann_state(HL, VL, HR, VR, a, g)
    assert Hs + a / g * Vs == pytest.approx(HL + a / g * VL, rel=1e-14)
    assert Hs - a / g * Vs == pytest.approx(HR - a / g * VR, rel=1e-14)


def test_minmod():
    assert minmod(np.array(1.0), np.array(2.0)) == 1.0
    assert minmod(np.array(-3.0), np.array(-2.0)) == -2.0
    assert minmod(np.array(1.0), np.array(-2.0)) == 0.0


# ---------------------------------------------------------------- Case 0
@pytest.mark.parametrize("order", [1, 2])
def test_case0_exact_Cap1(order):
    r = run_fvm(C0, Numerics(Ns=32, Cr=1.0, C_ap=1.0, order=order))
    ex = valve_head_exact(C0, r.t)
    m = away_from_fronts(C0, r.t)
    assert np.abs(r.H_cellN[m] - ex[m]).max() < 1e-9
    assert np.abs(r.H_valve[m] - ex[m]).max() < 1e-9


def test_case0_damping_monotone_in_Cap():
    """Numerical damping grows as C_-ap decreases (paper p. 5, Fig. 4)."""
    T = 4 * C0.L / C0.a
    amps = []
    for C in (1.0, 0.9, 0.5, 0.0):
        r = run_fvm(C0, Numerics(Ns=32, Cr=1.0, C_ap=C, order=2))
        late = r.t > 8 * T
        amps.append(r.H_cellN[late].max() - r.H_cellN[late].min())
    assert all(a1 >= a2 - 1e-6 for a1, a2 in zip(amps, amps[1:]))
    assert amps[-1] < amps[0] - 1.0


# ---------------------------------------------------------------- steady state
def test_steady_state_first_order():
    """With the valve open (Tc -> infinity) the steady state with friction is
    preserved up to the O(dt^2) splitting error of Eqs. (7)-(9)."""
    case = C1.with_(Tc=1e9)
    r = run_fvm(case, Numerics(Ns=32, Cr=1.0, C_ap=0.9, order=1), t_end=0.2)
    assert np.abs(r.H_cellN - r.H_cellN[0]).max() < 1e-3
    assert np.abs(r.V_valve - r.V_valve[0]).max() < 1e-5


def test_steady_state_second_order_small_drift():
    case = C1.with_(Tc=1e9)
    r = run_fvm(case, Numerics(Ns=32, Cr=1.0, C_ap=0.9, order=2), t_end=0.2)
    assert np.abs(r.H_cellN - r.H_cellN[0]).max() < 5e-3


# ---------------------------------------------------------------- conservation
@pytest.mark.parametrize("order", [1, 2])
def test_volume_conservation_without_cavities(order):
    """Liquid storage (gA/a^2) sum(H) dx changes only by boundary fluxes."""
    r = run_fvm(C0, Numerics(Ns=32, Cr=0.7, C_ap=1.0, order=order, model="none"))
    vol_scale = C0.area * C0.L
    assert np.abs(r.mass_error).max() / vol_scale < 1e-12


# ---------------------------------------------------------------- convergence
def _pulse_error(Ns, order, Cr=0.5):
    """Smooth Gaussian head pulse in a frictionless pipe; exact solution by
    d'Alembert; compared before the waves reach the boundaries.  Liquid at
    rest (V0 = 0) so that both boundaries are initially at equilibrium."""
    case = C0.with_(Tc=1e9, V0=0.0)
    L, a, g = case.L, case.a, case.fluid.g
    sig, amp, H0 = 3.0, 5.0, case.Hr

    def h0(x):
        return amp * np.exp(-((x - L / 2) / sig) ** 2)

    t_end = 0.25 * L / a
    r = run_fvm(case, Numerics(Ns=Ns, Cr=Cr, order=order, model="none"), t_end=t_end,
                record_profiles_at=(t_end,), initial=lambda x: (H0 + h0(x), 0.0 * x))
    (x, H, V, _), = r.meta["profiles"].values()
    tt = r.meta["dt"] * round(t_end / r.meta["dt"])
    Hex = H0 + 0.5 * (h0(x - a * tt) + h0(x + a * tt))
    return np.sqrt(np.mean((H - Hex) ** 2))


# MINMOD clips smooth extrema: observed order ~1.7 for the 2nd-order scheme
@pytest.mark.parametrize("order,expected", [(1, 1.0), (2, 1.9)])
def test_convergence_order(order, expected):
    e = [_pulse_error(Ns, order) for Ns in (128, 256, 512)]
    p = math.log(e[1] / e[2], 2)
    assert p > expected * 0.85, (e, p)


# ---------------------------------------------------------------- cavity relations
def test_method_I_gas_law_and_head_conservation():
    Ns = 4
    st = CavityState(Ns, np.zeros(Ns), -10.0, C3=3e-10)
    H = np.array([20., 22., 30., 26., 5., 7., 40., 41.])
    Q = np.zeros(2 * Ns)
    Hsum = H.sum()
    apply_dgcm(st, H, Q, 1e-4, 0.5)
    Hg = 0.5 * (H[0::2] + H[1::2])
    np.testing.assert_allclose(st.Vg * (Hg + 10.0), 3e-10, rtol=1e-12)   # Eq. (11)
    assert H.sum() == pytest.approx(Hsum, rel=1e-14)   # Eqs. (12)-(13) conserve sum H


def test_method_II_continuity_and_gas_law():
    st = CavityState(1, np.array([1.0]), -10.0, C3=3e-10)
    st.Vg[:] = 1e-8
    st.cav[:] = True
    H = np.array([-9.5, -9.4])
    Q = np.array([1e-5, 3e-5])
    dt = 4e-4
    apply_dgcm(st, H, Q, dt, 0.9)
    Vnew = 1e-8 + (3e-5 - 1e-5) * dt                                  # Eq. (15)
    assert st.Vg[0] == pytest.approx(Vnew, rel=1e-14)
    assert H[0] == H[1] == pytest.approx(3e-10 / Vnew + 1.0 - 10.0)   # Eqs. (16)-(17)


def test_dvcm_collapse():
    st = CavityState(1, np.array([0.0]), -10.0, C3=0.0)
    st.Vg[:] = 1e-9
    st.cav[:] = True
    H = np.array([5.0, 6.0])
    apply_dvcm(st, H, np.array([1e-4, 0.0]), 1e-3)   # volume becomes negative
    assert not st.cav[0] and st.Vg[0] == 0.0 and H.tolist() == [5.0, 6.0]


# ---------------------------------------------------------------- valve
@pytest.mark.parametrize("Cp,tau", [(40.0, 0.5), (23.1, 1.0), (10.0, 0.3), (60.0, 0.01)])
def test_valve_orifice_law(Cp, tau):
    B, Vref, Hd, dH0 = 1280 / 9.81, 0.332, 23.0, 0.014
    V = valve_velocity(Cp, tau, Vref, Hd, dH0, B)
    H = Cp - B * V
    # residual of the orifice law written as V|V| dH0/(Vref tau)^2 = H - Hd
    res = V * abs(V) * dH0 / (Vref * tau) ** 2 - (H - Hd)
    assert abs(res) < 1e-11 * max(1.0, abs(Cp))


# ---------------------------------------------------------------- MOC
def test_moc_case0_matches_exact():
    r = run_moc_dgcm(C0, Ns=32, alpha0=1e-12)
    m = away_from_fronts(C0, r.t, 0.05)
    ex = valve_head_exact(C0, r.t)
    assert np.abs(r.H_valve[m] - ex[m]).max() < 1e-3


def test_moc_steady_state():
    r = run_moc_dgcm(C1.with_(Tc=1e9), Ns=32, t_end=0.1)
    assert np.abs(r.H_valve - r.H_valve[0]).max() < 1e-6


# ---------------------------------------------------------------- dimensional checks
def test_similarity_L_over_a():
    """Frictionless system: H(t) depends on L and a only through L/a."""
    r1 = run_fvm(C0, Numerics(Ns=32, Cr=1.0, C_ap=0.5), t_end=0.3)
    c2 = C0.with_(L=2 * C0.L, a=2 * C0.a, V0=C0.V0 / 2)   # same aV0/g and L/a
    r2 = run_fvm(c2, Numerics(Ns=32, Cr=1.0, C_ap=0.5), t_end=0.3)
    np.testing.assert_allclose(r1.H_cellN, r2.H_cellN, atol=1e-9)


def test_datum_invariance_with_cavitation():
    """Shifting the datum (Hr and z by the same constant) shifts every
    piezometric head by that constant: only H - z enters the physics."""
    r1 = run_fvm(C1, Numerics(Ns=32, Cr=1.0, C_ap=0.9), t_end=0.2)
    c2 = C1.with_(Hr=C1.Hr + 7.0, z0=7.0)
    r2 = run_fvm(c2, Numerics(Ns=32, Cr=1.0, C_ap=0.9), t_end=0.2)
    np.testing.assert_allclose(r2.H_cellN - 7.0, r1.H_cellN, atol=1e-7)


def test_vapour_head_definition():
    fl = Fluid()
    assert fl.Hv == pytest.approx(fl.p_vap / (fl.rho * fl.g) - fl.p_bar / (fl.rho * fl.g))
    assert -10.2 < fl.Hv < -10.0
