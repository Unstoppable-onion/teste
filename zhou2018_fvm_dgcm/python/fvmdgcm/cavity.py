"""Discrete cavity treatment at the middle of each reach (paper pp. 3-4).

Reach j (0-based here) is made of the cells u = 2j (upstream half, H_uj,
Q_uj) and d = 2j+1 (downstream half, H_j, Q_j); the cavity sits on the
interface between them, at x_j = (2j+1) dx, elevation z(j).

DGCM (this paper), flowchart Fig. 3:
  * Method II is used when cavitation existed at t, or when the FVM head of
    one of the halves is at/below the vapour head z(j)+Hv:
        Vg^{n+1} = Vg^n + (Q_j - Q_uj) dt                         (15)
        Hg = p0 alpha0 Vol / (rho g Vg^{n+1}) + z(j) + Hv          (16)
        H_uj = H_j = Hg                                            (17)
  * otherwise (or if the cavity does not exist at t+dt) Method I:
        Hg = (H_uj + H_j)/2                                        (10)
        Vg = p0 alpha0 Vol / [rho g (Hg - z(j) - Hv)]              (11)
        H_uj <- C H_uj + (1-C) Hg ;  H_j <- C H_j + (1-C) Hg       (12-13)

"Does cavitation exist at t+dt?" is not defined explicitly in the paper
[DED].  Implemented criteria (``collapse``):
  "volume"   : the cavity exists while Vg^{n+1} > 0 (classic DVCM
               collapse criterion; Wylie et al. 1993, Bergant et al. 2006);
  "pressure" : additionally, a cavity that already existed at t collapses
               when the gas head of Eq. (16) exceeds the mean FVM head of the
               two halves (the liquid pressure no longer sustains it).

Two further interpretation choices are needed [DED] (docs, section 8.5):
  * ``limit_growth`` (default on): in Method I the free-gas volume of
    Eq. (11) may not grow faster than continuity allows,
    Vg <= Vg^n + max(Vnew - Vg^n, 0).  Literal Eq. (11) makes Vg -> infinity
    when the mean head approaches the vapour head, which pumps spurious
    cavity volume into the next Method II step; with Ns = 256 this delays
    the first collapse by 9-11 ms, contrary to the paper's Figs. 6 and 8.
  * ``fallback``: when continuity gives Vg <= 0 while the mean head is at or
    below the vapour head, neither method applies; "keep" (default) keeps
    the cavity with its previous volume, "collapse" collapses it as in the
    DVCM (heads not clamped, gas back to its initial volume).

DVCM (Zhou et al. 2017, used for Fig. 10): same logic with pure vapour
(Hg = z(j)+Hv, no free gas), the cavity volume being zero when absent and
the FVM heads being left untouched (no adjustment) without cavitation.
"""
from __future__ import annotations

import numpy as np


class CavityState:
    def __init__(self, Ns: int, zc: np.ndarray, Hv: float, C3: float):
        self.Ns = Ns
        self.hvap = zc + Hv                 # vapour piezometric head at each cavity
        self.C3 = C3                        # p0 alpha0 Vol / (rho g)  [m^4]
        self.Vg = np.zeros(Ns)              # cavity (gas+vapour) volume, m^3
        self.cav = np.zeros(Ns, dtype=bool)  # "cavitation exists" flag
        self.n_fallback = 0                 # diagnostics (see apply_dgcm)
        self.limit_growth = False           # continuity-limited Method I volume [DED]
        self.fallback = "keep"              # treatment of an impossible Method I [DED]
        self.Vg_init = np.zeros(Ns)

    def init_equilibrium(self, H: np.ndarray):
        Hu, Hd = H[0::2], H[1::2]
        Hg = 0.5 * (Hu + Hd)
        if self.C3 > 0:
            self.Vg = self.C3 / (Hg - self.hvap)
            self.Vg_init = self.Vg.copy()


def apply_dgcm(st: CavityState, H: np.ndarray, Q: np.ndarray, dt: float, C_ap: float,
               collapse: str = "volume") -> None:
    """In-place DGCM correction of the FVM heads H (length 2 Ns)."""
    Hu, Hd = H[0::2].copy(), H[1::2].copy()
    Qu, Qd = Q[0::2], Q[1::2]
    hv = st.hvap
    Hbar = 0.5 * (Hu + Hd)

    use2 = st.cav | (np.minimum(Hu, Hd) <= hv)
    Vnew = st.Vg + (Qd - Qu) * dt                          # Eq. (15)
    with np.errstate(divide="ignore", invalid="ignore"):
        Hg2 = st.C3 / Vnew + hv                            # Eq. (16)
    exists = use2 & (Vnew > 0.0)
    if collapse == "pressure":
        exists &= ~(st.cav & (Hbar > hv) & (Hg2 > Hbar))

    # Method I where no cavitation at t+dt.  If Method I is impossible
    # (mean head at/below vapour: Eq. 11 would give a negative volume) the
    # cavity is kept with its previous volume (counted as fallback).
    m1 = ~exists
    bad = m1 & (Hbar <= hv)
    if np.any(bad):
        st.n_fallback += int(bad.sum())
        m1 &= ~bad
        if st.fallback == "keep":
            # keep the cavity with its previous volume
            Hg_keep = st.C3 / st.Vg + hv
            Hu[bad] = Hd[bad] = Hg_keep[bad]
            st.cav[bad] = True
        else:
            # "collapse": the cavity has collapsed (continuity) - as in the
            # DVCM the FVM heads are kept (Eqs. 12-13 with the mean head) and
            # the free gas returns to its initial (steady-state) volume
            Hb_ = Hbar[bad]
            Hu[bad] = C_ap * Hu[bad] + (1.0 - C_ap) * Hb_
            Hd[bad] = C_ap * Hd[bad] + (1.0 - C_ap) * Hb_
            st.Vg[bad] = st.Vg_init[bad] if st.fallback == "collapse" else st.Vg[bad]
            st.cav[bad] = False

    # Method II results
    Hu[exists] = Hg2[exists]
    Hd[exists] = Hg2[exists]
    st.Vg[exists] = Vnew[exists]
    st.cav[exists] = True

    # Method I results
    if np.any(m1):
        Hg1 = Hbar[m1]
        Veq = st.C3 / (Hg1 - hv[m1])                        # Eq. (11)
        if st.limit_growth:
            # [DED] regularisation: the free gas cannot expand faster than
            # the liquid makes room for it (continuity, Eq. 15)
            Veq = np.minimum(Veq, st.Vg[m1] + np.maximum(Vnew[m1] - st.Vg[m1], 0.0))
        st.Vg[m1] = Veq
        Hu[m1] = C_ap * Hu[m1] + (1.0 - C_ap) * Hg1         # Eq. (12)
        Hd[m1] = C_ap * Hd[m1] + (1.0 - C_ap) * Hg1         # Eq. (13)
        st.cav[m1] = False
    H[0::2], H[1::2] = Hu, Hd


def apply_dvcm(st: CavityState, H: np.ndarray, Q: np.ndarray, dt: float) -> None:
    """In-place discrete vapour cavity correction (FVM-DVCM)."""
    Hu, Hd = H[0::2].copy(), H[1::2].copy()
    Qu, Qd = Q[0::2], Q[1::2]
    hv = st.hvap
    use = st.cav | (np.minimum(Hu, Hd) <= hv)
    Vnew = st.Vg + (Qd - Qu) * dt
    exists = use & (Vnew > 0.0)
    Hu[exists] = hv[exists]
    Hd[exists] = hv[exists]
    st.Vg = np.where(exists, Vnew, 0.0)
    st.cav = exists
    H[0::2], H[1::2] = Hu, Hd
