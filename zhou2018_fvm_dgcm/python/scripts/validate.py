"""Quantitative validation of every run against the digitised paper data.

For each run of the registry:
  * pointwise errors vs the paper's numerical curve (flat parts and all);
  * plateau heads and pulse peaks in fixed windows (FEATURES);
  * event timings (crossings of the case level) paired with the paper's;
  * the same metrics vs the digitised experiment (secondary, informative);
  * Case 0: error vs the exact solution.

Acceptance criteria (justified in docs/relatorio_validacao.md, sec. 3):
  T_FLAT   median |dH| on flat parts            <= 3 px of the figure (~1.1-1.5 m)
  T_PLAT   |dH| of plateau heads                <= 3 px
  T_EVT1   |dt| of the first two paired events   <= 1.5 ms (3 px)
  T_EVT    mean |dt| of all paired events        <= 2.5 ms
  T_EVTN   fraction of the paper's events paired  >= 75 %
  T_PEAK   |dH| of pulse peaks                   <= max(5 m, 10 % of the peak)
Status: VALIDADO (all criteria hold); PARCIAL (bulk criteria T_FLAT, T_PLAT,
T_EVT1, T_EVT hold but pulse peaks/spikes differ); DIVERGENTE (a bulk
criterion fails); NAO_AVALIAVEL (paper series hidden behind other curves:
visible in < 20 % of the time axis); series visible in 20-60 % are
compared on their visible parts only (flag 'visibility' = 'parcial').

Usage: python -m scripts.validate [--sim-dir results/python] [--tag python]
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from fvmdgcm.exact import valve_head_exact
from fvmdgcm.experiments import EXPERIMENT, FEATURES, RUNS
from fvmdgcm.metrics import (crossings_dig, crossings_sim, load_digitized, pair_events,
                             pointwise, window_extreme, window_median)
from fvmdgcm.params import CASES

ROOT = Path(__file__).resolve().parents[2]
# series visible in less than this fraction of the time axis are hidden
# behind other curves of the same figure and cannot be compared
MIN_COVERAGE = 0.2
# between MIN and FULL coverage the series is compared on its visible parts
FULL_COVERAGE = 0.6


def load_sim(sim_dir: Path, run_id: str):
    rows = list(csv.DictReader(open(sim_dir / f"{run_id}.csv")))
    t = np.array([float(r["t_s"]) for r in rows])
    H = np.array([float(r["H_m"]) for r in rows])
    return t, H


def compare(t, H, dig, case_name, tol_px=3.0):
    feat = FEATURES[case_name]
    res = {"pointwise": pointwise(t, H, dig)}
    px = dig["dH_px"]
    crit = {}
    res["flat_medae_tol"] = tol_px * px
    crit["T_FLAT"] = res["pointwise"]["flat"]["medae"] <= tol_px * px
    plats = {}
    for name, t0, t1 in feat["plateaus"]:
        p = window_median(dig["t"], dig["H"], t0, t1)
        s = window_median(t, H, t0, t1)
        plats[name] = dict(paper=p, sim=s, diff=s - p, ok=bool(abs(s - p) <= tol_px * px))
    res["plateaus"] = plats
    if plats:
        crit["T_PLAT"] = all(v["ok"] for v in plats.values() if np.isfinite(v["paper"]))
    peaks = {}
    for name, t0, t1 in feat["peaks"]:
        p = window_extreme(dig["t"], dig["Hmax"], t0, t1, "max")
        s = window_extreme(t, H, t0, t1, "max")
        tol = max(5.0, 0.10 * abs(p))
        peaks[name] = dict(paper=p, sim=s, diff=s - p, tol=tol, ok=bool(abs(s - p) <= tol))
    res["peaks"] = peaks
    if peaks:
        crit["T_PEAK"] = all(v["ok"] for v in peaks.values() if np.isfinite(v["paper"]))
    lev = feat["level"]
    ev_p = crossings_dig(dig, lev)
    ev_s = crossings_sim(t, H, lev)
    pairs = pair_events(ev_p, ev_s)
    res["events"] = dict(level=lev, paper=ev_p.tolist(), sim=ev_s.tolist(), pairs=pairs)
    if pairs:
        d = np.array([p[2] for p in pairs])
        res["events"].update(mean_abs_ms=float(1e3 * np.mean(np.abs(d))),
                             max_abs_ms=float(1e3 * np.max(np.abs(d))),
                             first2_max_abs_ms=float(1e3 * np.max(np.abs(d[:2]))),
                             n_paper=int(ev_p.size), n_paired=len(pairs))
        crit["T_EVT1"] = res["events"]["first2_max_abs_ms"] <= 1.5
        crit["T_EVT"] = res["events"]["mean_abs_ms"] <= 2.5
    if ev_p.size:
        # at least 75 % of the paper's events must have a counterpart within 10 ms
        res["events"]["paired_fraction"] = len(pairs) / ev_p.size
        crit["T_EVTN"] = res["events"]["paired_fraction"] >= 0.75
    res["criteria"] = {k: bool(v) for k, v in crit.items()}
    res["coverage"] = dig["coverage"]
    bulk = [v for k, v in crit.items() if k != "T_PEAK"]
    res["visibility"] = "total" if dig["coverage"] >= FULL_COVERAGE else "parcial"
    if dig["coverage"] < MIN_COVERAGE:
        res["status"] = "NAO_AVALIAVEL"
    elif not all(bulk):
        res["status"] = "DIVERGENTE"
    elif not crit.get("T_PEAK", True):
        res["status"] = "PARCIAL"
    else:
        res["status"] = "VALIDADO"
    return res


def main(sim_dir: Path, tag: str):
    out = {}
    for run in RUNS:
        rid = run["id"]
        t, H = load_sim(sim_dir, rid)
        case = CASES[run["case"]]
        entry = {"fig": run["fig"], "case": run["case"], "solver": run["solver"],
                 "num": run["num"], "dig": run["dig"]}
        dig = load_digitized(run["dig"])
        entry["vs_paper"] = compare(t, H, dig, run["case"])
        if run["case"] == "case0" and run["solver"] != "exact":
            ex = valve_head_exact(case, t)
            T2 = 2 * case.L / case.a
            ph = (t / T2) % 1.0
            m = (ph > 0.02) & (ph < 0.98) & (t > 0)
            entry["vs_exact"] = dict(max_abs_err_away_from_fronts=float(np.abs(H[m] - ex[m]).max()),
                                     rmse_all=float(np.sqrt(np.mean((H - ex) ** 2))))
            # extrema of the last period (numerical damping)
            Tp = 4 * case.L / case.a
            late = t > 8 * Tp + 0.005
            dl = dig["t"] > 8 * Tp + 0.005
            entry["late_period"] = dict(sim_max=float(H[late].max()), sim_min=float(H[late].min()),
                                        paper_max=float(dig["H"][dl].max()),
                                        paper_min=float(dig["H"][dl].min()))
        key = run["fig"] + (run["id"][5] if run["fig"] == "fig06" else "")
        if key in EXPERIMENT:
            entry["vs_experiment"] = compare(t, H, load_digitized(EXPERIMENT[key]), run["case"])
        out[rid] = entry
        vp = entry["vs_paper"]
        print(f"{rid:16s} {vp['status']:10s} flatMedAE={vp['pointwise']['flat']['medae']:.2f} m "
              f"evt={vp.get('events', {}).get('mean_abs_ms', float('nan')):.2f} ms "
              f"crit={vp['criteria']}")
    dest = ROOT / "results" / "validation"
    dest.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(dest / f"metrics_{tag}.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim-dir", default=str(ROOT / "results" / "python"))
    ap.add_argument("--tag", default="python")
    a = ap.parse_args()
    main(Path(a.sim_dir), a.tag)
