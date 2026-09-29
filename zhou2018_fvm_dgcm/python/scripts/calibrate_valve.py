"""Inference of the (unreported) steady head loss of the open valve.

The paper only states that the ball-valve closure is "simply considered as a
linear closure" with effective closing time Tc (Table 1).  With the standard
orifice law V = V0 tau sqrt(dH/dH0), tau = 1 - t/Tc, the instant at which the
flow effectively stops (and the head rises by aV0/g) depends on the steady
valve loss dH0 = K V0^2/(2g), which is not given.

Procedure (documented in docs/analise_do_artigo.md, section 8.4):
  1. t50 = time at which the valve head crosses the mid level of its first
     rise, measured on the paper's own FVM-DGCM curves (line-centre
     crossing, Figs. 5, 6a-d for Case 1; Fig. 7 for Case 2; Fig. 8 Case 3);
  2. K of the Simpson (1986) apparatus is fitted on Case 1 only;
  3. Case 2 (same apparatus and valve) is an independent check: its t50 is
     *predicted* with the Case-1 K;
  4. K of the Bergant & Simpson (1999) apparatus (Case 3) is fitted
     separately (no independent check possible).

Usage: python -m scripts.calibrate_valve   (writes results/valve_calibration.json)
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from fvmdgcm.fvm_solver import run_fvm
from fvmdgcm.metrics import crossings_dig, crossings_sim, load_digitized
from fvmdgcm.params import CASES, Numerics

ROOT = Path(__file__).resolve().parents[2]

TARGETS = {
    "case1": dict(keys=["fig05_main_a1e-7", "fig06_a_Ns32", "fig06_b_Ns32", "fig06_c_Ns32",
                        "fig06_d_Ns32"], Ns=32, C_ap=0.9),
    "case2": dict(keys=["fig07_main_Cap0.9"], Ns=32, C_ap=0.9),
    "case3": dict(keys=["fig08_main_Cap0.9"], Ns=256, C_ap=0.9),
}


def mid_level(case):
    H0 = case.Hr - case.friction * case.L * case.V0 ** 2 / (2 * case.fluid.g * case.D)
    return H0 + 0.5 * case.joukowsky


def paper_t50(name):
    case = CASES[name]
    lev = mid_level(case)
    vals = []
    for k in TARGETS[name]["keys"]:
        c = crossings_dig(load_digitized(k), lev, 0.0, case.Tc + 0.01)
        vals.append(float(c[0]))
    return lev, vals


def model_t50(name, K):
    case = CASES[name]
    case = case.with_(K_valve=K)
    tg = TARGETS[name]
    r = run_fvm(case, Numerics(Ns=tg["Ns"], Cr=1.0, C_ap=tg["C_ap"], order=2),
                t_end=case.Tc + 0.01)
    return float(crossings_sim(r.t, r.H_cellN, mid_level(case))[0])


def fit_K(name, target, lo=0.01, hi=3000.0, it=40):
    """Bisection on log K (t50 decreases monotonically with K)."""
    for _ in range(it):
        mid = math.sqrt(lo * hi)
        if model_t50(name, mid) > target:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


def main():
    out = {}
    for name in ("case1", "case2", "case3"):
        lev, vals = paper_t50(name)
        out[name] = dict(level=lev, paper_t50=vals, paper_t50_mean=float(np.mean(vals)),
                         paper_t50_sd=float(np.std(vals)))
    K1 = fit_K("case1", out["case1"]["paper_t50_mean"])
    # sensitivity of K1 to +-1 sd / +-0.5 ms (digitisation) of the target
    K1_lo = fit_K("case1", out["case1"]["paper_t50_mean"] + 0.0005)
    K1_hi = fit_K("case1", out["case1"]["paper_t50_mean"] - 0.0005)
    out["case1"].update(K_fit=K1, K_range_pm0p5ms=[K1_lo, K1_hi],
                        model_t50=model_t50("case1", K1))
    t2 = model_t50("case2", K1)
    out["case2"].update(K_used=K1, model_t50_predicted=t2,
                        error_ms=1e3 * (t2 - out["case2"]["paper_t50_mean"]))
    K3 = fit_K("case3", out["case3"]["paper_t50_mean"])
    out["case3"].update(K_fit=K3, model_t50=model_t50("case3", K3))
    for name in out:
        c = CASES[name]
        K = out[name].get("K_fit", out[name].get("K_used"))
        out[name]["dH_valve0"] = K * c.V0 ** 2 / (2 * c.fluid.g)
    path = ROOT / "results" / "valve_calibration.json"
    path.parent.mkdir(exist_ok=True, parents=True)
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
