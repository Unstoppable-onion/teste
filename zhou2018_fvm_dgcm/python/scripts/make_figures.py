"""Reproduce Figs. 4-11 of Zhou et al. (2018) and overlay the digitised
paper curves (thin grey dots) for direct visual comparison.

Output: results/figures/figNN.png (reproduced figure, same layout/axes as the
paper) and results/figures/figNN_compare.png (each simulated series vs the
digitised paper series and experiment).

Usage: python -m scripts.make_figures [--sim-dir results/python] [--suffix ""]
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from fvmdgcm.experiments import EXPERIMENT, RUNS  # noqa: E402
from fvmdgcm.metrics import load_digitized  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PAPER_STYLE = dict(color="#7a7a7a", ms=1.6, marker=".", ls="none")
EXP_STYLE = dict(color="black", lw=2.2)
COLS = {"red": "#d62728", "blue": "#1f3fbf", "grey": "#8c8c8c", "black": "black"}


def load(sim_dir, rid):
    rows = list(csv.DictReader(open(sim_dir / f"{rid}.csv")))
    return (np.array([float(r["t_s"]) for r in rows]), np.array([float(r["H_m"]) for r in rows]))


def exp_curve(key):
    d = load_digitized(key)
    return d["t"], d["H"]


def panel(ax, sim_dir, series, exp_key=None, xlim=(0, 0.45), ylim=(-20, 160), yt=None,
          title=None, show_paper=True):
    if exp_key:
        t, H = exp_curve(exp_key)
        ax.plot(t, H, label="Experiment (digitised)", **EXP_STYLE)
    for rid, label, col, lw, ls in series:
        t, H = load(sim_dir, rid)
        ax.plot(t, H, color=COLS[col], lw=lw, ls=ls, label=label)
    if show_paper:
        first = True
        for rid, *_ in series:
            run = next(r for r in RUNS if r["id"] == rid)
            d = load_digitized(run["dig"])
            ax.plot(d["t"], d["H"], label="paper (digitised)" if first else None, **PAPER_STYLE)
            first = False
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if yt is not None:
        ax.set_yticks(yt)
    ax.set_xlabel("t (s)")
    ax.set_ylabel("H (m)")
    if title:
        ax.set_title(title, fontsize=9, loc="left")
    ax.legend(fontsize=7, loc="upper right", frameon=False)


def make(sim_dir: Path, out: Path, suffix: str):
    out.mkdir(parents=True, exist_ok=True)
    Y1 = [-20, 20, 60, 100, 140]
    # Fig 4
    fig, axs = plt.subplots(2, 2, figsize=(12, 7))
    for ax, p, C in zip(axs.flat, "abcd", (1.0, 0.9, 0.5, 0.0)):
        panel(ax, sim_dir, [(f"fig04{p}_exact", "Exact", "grey", 2.5, "-"),
                            (f"fig04{p}_o2", "2nd FVM-DGCM", "red", 1.2, ":"),
                            (f"fig04{p}_o1", "1st FVM-DGCM", "blue", 0.8, "-")],
              xlim=(0, 1), ylim=(0, 60), yt=[0, 20, 40, 60],
              title=f"({p}) Case 0, $C_{{-ap}}$ = {C}, Ns = 32, Cr = 1")
    fig.tight_layout(); fig.savefig(out / f"fig04{suffix}.png", dpi=130); plt.close(fig)
    # Fig 5
    fig, ax = plt.subplots(figsize=(7, 4))
    panel(ax, sim_dir, [("fig05_a1e-10", r"2nd FVM-DGCM $\alpha_0$=1e-10", "grey", 1.2, "-"),
                        ("fig05_a1e-8", r"2nd FVM-DGCM $\alpha_0$=1e-8", "red", 1.2, "-"),
                        ("fig05_a1e-7", r"2nd FVM-DGCM $\alpha_0$=1e-7", "blue", 1.2, "-")],
          exp_key=EXPERIMENT["fig05"], yt=Y1, title="Fig. 5 - Case 1")
    fig.tight_layout(); fig.savefig(out / f"fig05{suffix}.png", dpi=130); plt.close(fig)
    # Fig 6
    fig, axs = plt.subplots(2, 2, figsize=(12, 7))
    for ax, p, C in zip(axs.flat, "abcd", (1.0, 0.9, 0.8, 0.5)):
        panel(ax, sim_dir, [(f"fig06{p}_Ns256", "2nd FVM-DGCM (Ns=256)", "grey", 1.0, "-"),
                            (f"fig06{p}_Ns32", "2nd FVM-DGCM (Ns=32)", "red", 1.2, "-")],
              exp_key=EXPERIMENT[f"fig06{p}"], yt=Y1, title=f"({p}) Case 1, $C_{{-ap}}$ = {C}")
    fig.tight_layout(); fig.savefig(out / f"fig06{suffix}.png", dpi=130); plt.close(fig)
    # Fig 7
    fig, ax = plt.subplots(figsize=(7, 4))
    panel(ax, sim_dir, [("fig07_Cap1.0", "2nd FVM-DGCM ($C_{-ap}$=1.0)", "grey", 1.8, "-"),
                        ("fig07_Cap0.9", "2nd FVM-DGCM ($C_{-ap}$=0.9)", "red", 1.2, "-")],
          exp_key=EXPERIMENT["fig07"], ylim=(-20, 230), yt=[-20, 30, 80, 130, 180, 230],
          title="Fig. 7 - Case 2 (Ns = 32)")
    fig.tight_layout(); fig.savefig(out / f"fig07{suffix}.png", dpi=130); plt.close(fig)
    # Fig 8
    fig, ax = plt.subplots(figsize=(7, 4))
    panel(ax, sim_dir, [("fig08_Cap1.0", "2nd FVM-DGCM ($C_{-ap}$=1.0)", "grey", 1.8, "-"),
                        ("fig08_Cap0.9", "2nd FVM-DGCM ($C_{-ap}$=0.9)", "red", 1.2, "-")],
          exp_key=EXPERIMENT["fig08"], xlim=(0, 0.57), ylim=(-20, 140),
          yt=[-20, 10, 40, 70, 100, 130], title="Fig. 8 - Case 3 (Ns = 256)")
    fig.tight_layout(); fig.savefig(out / f"fig08{suffix}.png", dpi=130); plt.close(fig)
    # Fig 9
    fig, axs = plt.subplots(2, 1, figsize=(7, 7))
    for ax, p, o in zip(axs, "ab", ("1st", "2nd")):
        panel(ax, sim_dir, [(f"fig09{p}_Cr1.0", f"{o} FVM-DGCM (Cr=1.0)", "black", 1.2, "-"),
                            (f"fig09{p}_Cr0.5", f"{o} FVM-DGCM (Cr=0.5)", "red", 1.2, "-"),
                            (f"fig09{p}_Cr0.1", f"{o} FVM-DGCM (Cr=0.1)", "blue", 1.2, "-")],
              yt=Y1, title=f"({p}) Case 1, $C_{{-ap}}$ = 0.9, {o} order")
    fig.tight_layout(); fig.savefig(out / f"fig09{suffix}.png", dpi=130); plt.close(fig)
    # Fig 10, 11
    for fid, lab in (("fig10", "2nd FVM-DVCM"), ("fig11", "MOC-DGCM")):
        fig, ax = plt.subplots(figsize=(7, 4))
        panel(ax, sim_dir, [(f"{fid}_Ns256", f"{lab} (Ns=256)", "grey", 1.0, "-"),
                            (f"{fid}_Ns32", f"{lab} (Ns=32)", "red", 1.2, "-")],
              exp_key=EXPERIMENT[fid], yt=Y1, title=f"Fig. {fid[-2:]} - Case 1")
        fig.tight_layout(); fig.savefig(out / f"{fid}{suffix}.png", dpi=130); plt.close(fig)

    # one comparison plot per run (simulation vs its digitised paper series)
    cmp_dir = out / "per_run"
    cmp_dir.mkdir(exist_ok=True)
    for run in RUNS:
        t, H = load(sim_dir, run["id"])
        d = load_digitized(run["dig"])
        fig, ax = plt.subplots(figsize=(9, 3.4))
        ax.fill_between(d["t"], d["Hmin"], d["Hmax"], color="0.8", step="mid",
                        label="paper: pixel extent")
        ax.plot(d["t"], d["H"], ".", color="0.35", ms=2, label="paper: digitised median")
        ax.plot(t, H, "-", color=COLS["red"], lw=0.9, label="this reproduction")
        ax.set_xlabel("t (s)"); ax.set_ylabel("H (m)")
        ax.set_title(f"{run['id']}  ({run['case']}, {run['solver']}, {run['num']})", fontsize=8)
        ax.legend(fontsize=7, frameon=False)
        fig.tight_layout(); fig.savefig(cmp_dir / f"{run['id']}{suffix}.png", dpi=110); plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim-dir", default=str(ROOT / "results" / "python"))
    ap.add_argument("--out", default=str(ROOT / "results" / "figures"))
    ap.add_argument("--suffix", default="")
    a = ap.parse_args()
    make(Path(a.sim_dir), Path(a.out), a.suffix)
