"""Physical and numerical parameters of Zhou et al. (2018), J. Hydraul. Eng. 144(5).

Every value is tagged with its origin:
  [T1]   Table 1 of the paper (p. 04018017-4)
  [TXT]  text of the paper (page given)
  [DED]  deduced (documented in docs/analise_do_artigo.md, section 8)

All quantities in SI units (m, s, kg, Pa); heads in metres of water.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

G = 9.81  # gravitational acceleration, m/s^2 [DED: standard value]


@dataclass(frozen=True)
class Fluid:
    """Water properties.  The paper does not report temperature, density,
    vapour pressure nor barometric pressure [DED]: water at 20 degC and the
    standard atmosphere are assumed."""

    rho: float = 998.2        # density, kg/m^3 (20 degC)
    nu: float = 1.004e-6      # kinematic viscosity, m^2/s (20 degC) - Blasius friction
    p_vap: float = 2339.0     # absolute vapour pressure, Pa (20 degC)
    p_bar: float = 101325.0   # absolute barometric pressure, Pa (standard atmosphere)
    p0: float = 101325.0      # standard (reference) pressure of alpha0, Pa [TXT p.2: p0*]
    g: float = G

    @property
    def Hb(self) -> float:
        """Absolute barometric pressure head, m [TXT p.2, after Eq. 2]."""
        return self.p_bar / (self.rho * self.g)

    @property
    def Hv(self) -> float:
        """Gauge vapour pressure head Hv = p_v*/(rho g) - Hb, m [TXT p.2]."""
        return self.p_vap / (self.rho * self.g) - self.Hb

    @property
    def H0_std(self) -> float:
        """p0*/(rho g): standard pressure head used with alpha0 (Eqs. 11, 16)."""
        return self.p0 / (self.rho * self.g)


def blasius(V: float, D: float, nu: float) -> float:
    """Darcy friction factor of a hydraulically smooth pipe (Blasius,
    4e3 < Re < 1e5).  Used because the paper does not give f [DED]."""
    Re = abs(V) * D / nu
    return 0.316 / Re ** 0.25


@dataclass(frozen=True)
class Case:
    """One case of Table 1."""

    name: str
    V0: float            # initial steady velocity, m/s [T1]
    Hr: float            # upstream reservoir head, m [T1]
    Tc: float            # effective valve closing time, s [T1]
    D: float             # pipe inner diameter, m [T1]
    L: float             # pipe length, m [T1]
    a: float             # wave speed, m/s [T1]
    rise: float          # elevation of the valve above the pipe inlet, m [TXT p.4] (datum = inlet [DED])
    frictionless: bool = False
    t_end: float = 0.45  # simulated time = abscissa range of the figures, s
    f: float | None = None  # Darcy friction factor; None -> Blasius at V0 [DED]
    # loss coefficient of the open valve, dH0 = K V0^2/(2g) [DED]: inferred
    # from the paper's own numerical head rise (scripts/calibrate_valve.py)
    K_valve: float = 2.55
    fluid: Fluid = field(default_factory=Fluid)
    z0: float = 0.0      # elevation of the pipe inlet above the datum, m (datum = inlet)

    @property
    def dH_valve0(self) -> float:
        """Steady head loss across the fully open valve, m."""
        return self.K_valve * self.V0 ** 2 / (2.0 * self.fluid.g)

    @property
    def area(self) -> float:
        return math.pi * self.D ** 2 / 4.0

    @property
    def friction(self) -> float:
        if self.frictionless:
            return 0.0
        if self.f is not None:
            return self.f
        return blasius(self.V0, self.D, self.fluid.nu)

    @property
    def sin_theta(self) -> float:
        return self.rise / self.L

    def z(self, x):
        """Pipe elevation (datum at the upstream end/inlet), m."""
        return self.z0 + self.sin_theta * x

    @property
    def joukowsky(self) -> float:
        return self.a * self.V0 / self.fluid.g

    def with_(self, **kw) -> "Case":
        return replace(self, **kw)


# Table 1 of the paper.  Slopes: Cases 1-2 "1:36" (rise 1.0 m over 36 m),
# Case 3 "upward slope of 3.2 deg" (rise = 37.2 sin 3.2deg) [TXT p.4].
CASES: dict[str, Case] = {
    "case0": Case("case0", V0=0.16, Hr=23.41, Tc=0.0, D=0.01905, L=36.0, a=1280.0,
                  rise=0.0, frictionless=True, t_end=1.0),
    "case1": Case("case1", V0=0.332, Hr=23.41, Tc=0.022, D=0.01905, L=36.0, a=1280.0,
                  rise=36.0 / 36.0, t_end=0.45),
    "case2": Case("case2", V0=1.125, Hr=21.74, Tc=0.024, D=0.01905, L=36.0, a=1280.0,
                  rise=36.0 / 36.0, t_end=0.45),
    "case3": Case("case3", V0=0.30, Hr=22.0, Tc=0.009, D=0.02210, L=37.2, a=1319.0,
                  rise=37.2 * math.sin(math.radians(3.2)), t_end=0.57, K_valve=18.9),
}


@dataclass(frozen=True)
class Numerics:
    """Numerical options of the FVM-DGCM (paper notation)."""

    Ns: int = 32              # number of reaches [TXT]; N = 2 Ns cells
    Cr: float = 1.0           # Courant number a dt / dx [TXT, Eq. after (9)]
    C_ap: float = 0.9         # pressure-adjustment coefficient C_-ap [Eqs. 12-13]
    alpha0: float = 1e-7      # gas void fraction at standard conditions [TXT]
    order: int = 2            # 1: Godunov first order; 2: MUSCL-Hancock + MINMOD
    model: str = "DGCM"       # "DGCM" (this paper) or "DVCM" (Zhou et al. 2017)
    # criterion for "Does cavitation exist at t+dt?" (Fig. 3) [DED, see docs]
    collapse: str = "volume"
    # continuity-limited free-gas expansion in Method I [DED, see docs]:
    # without it Eq. (11) creates spurious cavity volume when the mean head
    # approaches the vapour head (grid-dependent collapse times, Ns = 256)
    limit_gas_growth: bool = True
    # continuity gives Vg <= 0 while the mean head is at/below vapour, so
    # neither Method II nor Method I (Eq. 11) applies [DED, see docs]:
    # "keep" = keep cavity with previous volume; "collapse" = DVCM-like
    # collapse (heads not clamped, free gas back to its initial volume);
    # "collapse_keepV" = DVCM-like collapse keeping the previous gas volume
    fallback: str = "keep"
