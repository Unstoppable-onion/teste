"""Sensitivity of the reproduction to the parameters/choices NOT reported in
the paper (docs/analise_do_artigo.md, section 8) and to the interpretation
choices of the cavity algorithm.

For each variant the metrics against the paper's curves of Fig. 6(b)
(Case 1, Ns = 32 and 256, C_ap = 0.9) and Fig. 8 (Case 3, Ns = 256,
C_ap = 0.9) are recomputed: flat-part median absolute error and mean
absolute event-time error.

Output: results/validation/sensitivity_python.json
"""
from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from fvmdgcm.fvm_solver import run_fvm
from fvmdgcm.metrics import crossings_dig, crossings_sim, load_digitized, pair_events, pointwise
from fvmdgcm.params import CASES, Fluid, Numerics

ROOT = Path(__file__).resolve().parents[2]
TARGETS = [("case1", 32, "fig06_b_Ns32"), ("case1", 256, "fig06_b_Ns256"),
           ("case3", 256, "fig08_main_Cap0.9")]
RHO_G = 998.2 * 9.81


def variants():
    yield "baseline", {}, {}
    yield "f x 0.8", {"f_scale": 0.8}, {}
    yield "f x 1.2", {"f_scale": 1.2}, {}
    yield "Hb - 0.3 m (vapour head +0.3 m)", {"fluid": Fluid(p_bar=101325 - 0.3 * RHO_G)}, {}
    yield "Hb + 0.3 m (vapour head -0.3 m)", {"fluid": Fluid(p_bar=101325 + 0.3 * RHO_G)}, {}
    yield "K_valve x 0.1", {"K_scale": 0.1}, {}
    yield "K_valve x 10", {"K_scale": 10.0}, {}
    yield "a - 1 %", {"a_scale": 0.99}, {}
    yield "a + 1 %", {"a_scale": 1.01}, {}
    yield "no gas-growth limit (literal Eq. 11)", {}, {"limit_gas_growth": False}
    yield "collapse criterion 'pressure'", {}, {"collapse": "pressure"}
    yield "fallback 'collapse'", {}, {"fallback": "collapse"}
    yield "output = boundary state U_N+1/2", {"output": "boundary"}, {}


def main():
    out = {}
    for name, cmod, nmod in variants():
        res = {}
        for cname, Ns, key in TARGETS:
            case = CASES[cname]
            kw = {}
            if "f_scale" in cmod:
                kw["f"] = case.friction * cmod["f_scale"]
            if "K_scale" in cmod:
                kw["K_valve"] = case.K_valve * cmod["K_scale"]
            if "a_scale" in cmod:
                kw["a"] = case.a * cmod["a_scale"]
            if "fluid" in cmod:
                kw["fluid"] = cmod["fluid"]
            case = case.with_(**kw)
            num = replace(Numerics(Ns=Ns, Cr=1.0, C_ap=0.9, order=2), **nmod)
            r = run_fvm(case, num)
            H = r.H_valve if cmod.get("output") == "boundary" else r.H_cellN
            d = load_digitized(key)
            pw = pointwise(r.t, H, d)
            pr = pair_events(crossings_dig(d, 20.0), crossings_sim(r.t, H, 20.0))
            res[f"{cname}_Ns{Ns}"] = dict(
                flat_medae_m=round(pw["flat"]["medae"], 3),
                event_mean_abs_ms=round(1e3 * float(np.mean([abs(p[2]) for p in pr])), 3) if pr else None,
                n_events=len(pr), n_paper_events=int(crossings_dig(d, 20.0).size))
        out[name] = res
        print(f"{name:40s}", "  ".join(f"{k}: {v['flat_medae_m']:.2f} m / {v['event_mean_abs_ms']} ms"
                                       for k, v in res.items()))
    json.dump(out, open(ROOT / "results" / "validation" / "sensitivity_python.json", "w"), indent=1)


if __name__ == "__main__":
    main()
