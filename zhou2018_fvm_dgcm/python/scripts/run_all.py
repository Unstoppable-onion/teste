"""Run every simulation of the reproduction matrix (Figs. 4-11).

Output (results/python/):
  <run id>.csv        t_s, H_m (head plotted by the paper "at the valve" =
                      head of the last cell I_N for the FVM, valve node for
                      the MOC, exact solution for Case 0), plus H_boundary_m
                      (Riemann boundary state U_N+1/2) for the FVM
  runs_meta.json      numerical metadata of every run (dx, dt, f, Hv, ...)
  run_registry.json   run definitions + case parameters (read by MATLAB)

Usage: python -m scripts.run_all [--only fig06]
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np

from fvmdgcm.exact import valve_head_exact
from fvmdgcm.experiments import RUNS
from fvmdgcm.fvm_solver import run_fvm
from fvmdgcm.moc_dgcm import run_moc_dgcm
from fvmdgcm.params import CASES, Numerics

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "python"


def simulate(run: dict):
    case = CASES[run["case"]]
    if run["solver"] == "fvm":
        r = run_fvm(case, Numerics(**run["num"]))
        meta = {k: v for k, v in r.meta.items() if k != "profiles"}
        meta["mass_error_max"] = float(np.abs(r.mass_error).max())
        return r.t, r.H_cellN, r.H_valve, meta
    if run["solver"] == "moc":
        r = run_moc_dgcm(case, Ns=run["num"]["Ns"], alpha0=run["num"]["alpha0"])
        return r.t, r.H_valve, None, r.meta
    if run["solver"] == "exact":
        t = np.arange(20001) * (case.t_end / 20000)
        return t, valve_head_exact(case, t), None, {"case": case.name}
    raise ValueError(run["solver"])


def save(run_id, t, H, Hb, meta):
    with open(OUT / f"{run_id}.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["t_s", "H_m"] + (["H_boundary_m"] if Hb is not None else []))
        for k in range(t.size):
            row = [f"{t[k]:.8f}", f"{H[k]:.9f}"]
            if Hb is not None:
                row.append(f"{Hb[k]:.9f}")
            w.writerow(row)


def export_registry():
    cases = {}
    for name, c in CASES.items():
        d = asdict(c)
        d.update(area=c.area, friction=c.friction, dH_valve0=c.dH_valve0,
                 Hv=c.fluid.Hv, Hb=c.fluid.Hb, H0_std=c.fluid.H0_std)
        cases[name] = d
    json.dump({"cases": cases, "runs": RUNS, "numerics_defaults": asdict(Numerics())},
              open(OUT / "run_registry.json", "w"), indent=1)


def main(only=None):
    OUT.mkdir(parents=True, exist_ok=True)
    export_registry()
    meta_path = OUT / "runs_meta.json"
    allmeta = json.load(open(meta_path)) if meta_path.exists() else {}
    for run in RUNS:
        if only and not run["id"].startswith(only):
            continue
        t0 = time.time()
        t, H, Hb, meta = simulate(run)
        save(run["id"], t, H, Hb, meta)
        meta["cpu_s"] = time.time() - t0
        allmeta[run["id"]] = meta
        print(f"{run['id']:18s} {meta['cpu_s']:6.2f} s")
    json.dump(allmeta, open(meta_path, "w"), indent=1, default=float)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    main(ap.parse_args().only)
