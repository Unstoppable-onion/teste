"""Quantitative comparison between simulated and digitised curves.

Metrics (docs/relatorio_validacao.md, section 3):
  * pointwise errors at the digitised abscissae: RMSE, MAE, median absolute
    error (MedAE), maximum absolute error, restricted to the "flat" parts of
    the digitised curve (columns whose vertical extent is <= ``flat_px``
    pixels), because at a vertical front a sub-millisecond time shift gives
    an arbitrarily large head error;
  * event timings: instants at which the curve crosses a head level
    (line-centre estimate for the digitised curve, linear interpolation for
    the simulation), paired by nearest neighbour;
  * extrema in time windows (peak heads).
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DIG = ROOT / "data" / "digitized"


def load_digitized(key: str) -> dict:
    """``key`` = '<fig>_<panel>_<series>' (file stem in data/digitized)."""
    rows = list(csv.DictReader(open(DIG / f"{key}.csv")))
    arr = {k: np.array([float(r[k]) for r in rows]) for k in rows[0]}
    fig_panel = "_".join(key.split("_")[:2])
    meta = json.load(open(DIG / "digitization_meta.json"))[fig_panel]
    left, right = meta["frame_px"][0], meta["frame_px"][1]
    coverage = len(rows) / max(right - left - 6, 1)
    return {"t": arr["t_s"], "H": arr["H_med_m"], "Hmin": arr["H_min_m"],
            "Hmax": arr["H_max_m"], "dt_px": meta["t_per_px"], "dH_px": meta["H_per_px"],
            "calib_rms_H": meta["calib_rms_H"], "coverage": coverage}


def pointwise(t_sim, H_sim, dig: dict, flat_px: float = 4.0, tmin: float = 0.0,
              tmax: float = np.inf) -> dict:
    t, H = dig["t"], dig["H"]
    sel = (t >= tmin) & (t <= tmax)
    flat = sel & ((dig["Hmax"] - dig["Hmin"]) <= flat_px * dig["dH_px"])
    Hs = np.interp(t, t_sim, H_sim)
    out = {}
    for name, m in (("all", sel), ("flat", flat)):
        e = Hs[m] - H[m]
        out[name] = dict(n=int(m.sum()), rmse=float(np.sqrt(np.mean(e ** 2))),
                         mae=float(np.mean(np.abs(e))), medae=float(np.median(np.abs(e))),
                         maxae=float(np.max(np.abs(e))), bias=float(np.mean(e)))
    return out


def crossings_sim(t, H, level):
    s = H > level
    idx = np.nonzero(s[1:] != s[:-1])[0]
    return np.array([t[i] + (level - H[i]) / (H[i + 1] - H[i]) * (t[i + 1] - t[i]) for i in idx])


def crossings_dig(dig: dict, level: float, tmin=0.0, tmax=np.inf):
    """Line-centre crossing times: runs of consecutive pixel columns whose
    vertical extent contains ``level``; the mean abscissa of each run is the
    crossing time (unbiased with respect to the line width)."""
    t = dig["t"]
    m = (t >= tmin) & (t <= tmax)
    t, lo, hi = t[m], dig["Hmin"][m], dig["Hmax"][m]
    span = (lo <= level) & (hi >= level)
    out, i = [], 0
    step = np.median(np.diff(t)) if t.size > 1 else 1.0
    while i < t.size:
        if span[i]:
            j = i
            while j + 1 < t.size and span[j + 1] and t[j + 1] - t[j] < 1.5 * step:
                j += 1
            out.append(t[i:j + 1].mean())
            i = j + 1
        else:
            i += 1
    return np.array(out)


def pair_events(t_ref, t_sim, max_dt=0.01):
    """One-to-one pairing of event times: candidate pairs (reference,
    simulated) closer than ``max_dt`` are accepted greedily in order of
    increasing |dt| (each event used at most once); returned sorted by the
    reference time as (t_ref, t_sim, t_sim - t_ref)."""
    t_ref = np.asarray(t_ref, dtype=float)
    t_sim = np.asarray(t_sim, dtype=float)
    cand = [(abs(ts - tr), i, j) for i, tr in enumerate(t_ref) for j, ts in enumerate(t_sim)
            if abs(ts - tr) <= max_dt]
    cand.sort()
    used_r, used_s, pairs = set(), set(), []
    for _, i, j in cand:
        if i in used_r or j in used_s:
            continue
        used_r.add(i)
        used_s.add(j)
        pairs.append((float(t_ref[i]), float(t_sim[j]), float(t_sim[j] - t_ref[i])))
    return sorted(pairs)


def window_extreme(t, H, t0, t1, kind="max", min_points=5):
    m = (t >= t0) & (t <= t1)
    if m.sum() < min_points:
        return float("nan")
    return float(H[m].max() if kind == "max" else H[m].min())


def window_median(t, H, t0, t1, min_points=5):
    m = (t >= t0) & (t <= t1)
    return float(np.median(H[m])) if m.sum() >= min_points else float("nan")
