"""Quantitative check of the statements made in the text/conclusions of the
paper, using the simulations of results/python (run scripts.run_all first).

Output: results/validation/claims_python.json (+ printed summary).
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from fvmdgcm.experiments import EXPERIMENT
from fvmdgcm.metrics import crossings_dig, crossings_sim, load_digitized, pair_events, pointwise

ROOT = Path(__file__).resolve().parents[2]
SIM = ROOT / "results" / "python"


def load(rid):
    rows = list(csv.DictReader(open(SIM / f"{rid}.csv")))
    return np.array([float(r["t_s"]) for r in rows]), np.array([float(r["H_m"]) for r in rows])


def diff(r1, r2):
    """Differences between two simulated series (on the grid of r1)."""
    t1, H1 = load(r1)
    t2, H2 = load(r2)
    H2i = np.interp(t1, t2, H2)
    e1 = crossings_sim(t1, H1, 20.0)
    e2 = crossings_sim(t2, H2, 20.0)
    pairs = pair_events(e1, e2)
    return dict(max_abs=float(np.max(np.abs(H1 - H2i))), rms=float(np.sqrt(np.mean((H1 - H2i) ** 2))),
                event_shift_ms=[round(1e3 * p[2], 2) for p in pairs])


def peak(rid, t0, t1):
    t, H = load(rid)
    m = (t >= t0) & (t <= t1)
    return float(H[m].max())


def main():
    C = {}
    # 1. Case 0, C_ap = 1 reproduces the exact solution (Fig. 4a, conclusion 2)
    m = json.load(open(ROOT / "results" / "validation" / "metrics_python.json"))
    C["C1_case0_Cap1_exact"] = {o: m[f"fig04a_o{o}"]["vs_exact"]["max_abs_err_away_from_fronts"]
                                for o in (1, 2)}
    # 2. damping grows as C_ap decreases (Fig. 4b-d)
    C["C2_case0_last_period_extrema"] = {p: m[f"fig04{p}_o2"]["late_period"] for p in "abcd"}
    # 3. alpha0 <= 1e-7 gives basically identical results (Fig. 5, conclusion 4)
    C["C3_alpha0"] = {"1e-8_vs_1e-7": diff("fig05_a1e-7", "fig05_a1e-8"),
                      "1e-10_vs_1e-7": diff("fig05_a1e-7", "fig05_a1e-10")}
    # paper's own shifts between alpha0 curves (digitised, visible parts)
    ref = crossings_dig(load_digitized("fig05_main_a1e-7"), 20.0)
    C["C3_alpha0"]["paper_event_shift_ms"] = {
        a: [round(1e3 * p[2], 2) for p in pair_events(ref, crossings_dig(load_digitized(f"fig05_main_{a}"), 20.0))]
        for a in ("a1e-8", "a1e-10")}
    # 4. first and second order identical at Cr = 1 (Fig. 9, conclusion 6)
    C["C4_order_Cr1"] = diff("fig09a_Cr1.0", "fig09b_Cr1.0")
    # 5. Cr < 1: first order more dissipative, underestimates the maximum head
    C["C5_peak_2nd_pulse"] = {f"order{o}_Cr{cr}": peak(f"fig09{p}_Cr{cr}", 0.17, 0.215)
                              for p, o in (("a", 1), ("b", 2)) for cr in ("1.0", "0.5", "0.1")}
    # 6. FVM-DGCM with C_ap = 1 = FVM-DVCM (Figs. 6a and 10, conclusion 7)
    C["C6_DGCM_Cap1_vs_DVCM"] = {"Ns32": diff("fig06a_Ns32", "fig10_Ns32"),
                                 "Ns256": diff("fig06a_Ns256", "fig10_Ns256")}
    # 7. spikes grow with the grid (C_ap = 1, DVCM, MOC) and are damped by C_ap < 1
    C["C7_max_head_after_0.25s"] = {rid: peak(rid, 0.25, 0.45) for rid in (
        "fig06a_Ns32", "fig06a_Ns256", "fig06b_Ns32", "fig06b_Ns256", "fig06d_Ns32", "fig06d_Ns256",
        "fig10_Ns32", "fig10_Ns256", "fig11_Ns32", "fig11_Ns256")}
    # 8. agreement with the experiment as a function of C_ap (Fig. 6; C_ap=0.9 "best")
    exp = {}
    for p, cap in zip("abcd", ("1.0", "0.9", "0.8", "0.5")):
        d = load_digitized(EXPERIMENT[f"fig06{p}"])
        for Ns in (32, 256):
            t, H = load(f"fig06{p}_Ns{Ns}")
            pw = pointwise(t, H, d)
            ev = pair_events(crossings_dig(d, 20.0), crossings_sim(t, H, 20.0))
            exp[f"Cap{cap}_Ns{Ns}"] = dict(flat_medae=pw["flat"]["medae"], all_rmse=pw["all"]["rmse"],
                                           mean_abs_event_ms=float(1e3 * np.mean([abs(e[2]) for e in ev])))
    C["C8_vs_experiment_case1"] = exp
    # 9. MOC-DGCM: later cavity collapse than FVM-DGCM (Fig. 11 vs Fig. 6b)
    C["C9_MOC_vs_FVM_Ns32"] = diff("fig06b_Ns32", "fig11_Ns32")
    out = ROOT / "results" / "validation" / "claims_python.json"
    json.dump(C, open(out, "w"), indent=1)
    print(json.dumps(C, indent=1))


if __name__ == "__main__":
    main()
