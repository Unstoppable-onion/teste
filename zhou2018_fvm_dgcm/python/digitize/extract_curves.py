"""Colour-based digitisation of the curves in Figs. 4-11 of Zhou et al. (2018).

Procedure (documented in docs/relatorio_validacao.md, section "Digitalização"):

1. Axis calibration by spine + tick detection (``calibrate.py``).
2. Pixel classification by colour (legend colours of each figure):
   black = experiment (or Cr=1 curve in Fig. 9), grey, red, blue.
   Grey pixels within 2 px of a black pixel are discarded because the JPEG
   anti-aliasing of the thick black curve produces grey fringes.
3. For every pixel column inside the frame (legend boxes masked) the
   classified pixels give ``H_min``, ``H_max`` and ``H_med`` (median); a
   vertical front appears as a column with a large ``H_max - H_min``.
4. Output: ``data/digitized/<fig>_<panel>_<series>.csv`` with columns
   t, H_med, H_min, H_max, npix and a JSON file with the calibration and
   the resolution (s/px, m/px) that define the digitisation uncertainty.

Usage:  python -m digitize.extract_curves
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from .calibrate import calibrate, load_rgb
from .figconfig import FIGS

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "figures_raw"
OUT = ROOT / "data" / "digitized"


def colour_masks(img: np.ndarray) -> dict[str, np.ndarray]:
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    mx = img.max(axis=2)
    mn = img.min(axis=2)
    mean = img.mean(axis=2)
    black = (mean < 90) & (mx - mn < 45)
    red = (r > 150) & (g < 110) & (b < 110) & (r - g > 70)
    blue = (b > 120) & (r < 110) & (b - r > 50) & (b - g > 30)
    grey = (mean > 95) & (mean < 205) & (mx - mn < 28)
    # remove grey fringes of black lines (dilate black by 2 px)
    dil = black.copy()
    for dy in (-2, -1, 0, 1, 2):
        for dx in (-2, -1, 0, 1, 2):
            dil |= np.roll(np.roll(black, dy, axis=0), dx, axis=1)
    grey &= ~dil
    return {"black": black, "red": red, "blue": blue, "grey": grey}


def digitise_panel(img, axes, mask: np.ndarray, legend_boxes, margin: int = 3):
    left, right, top, bottom = axes.frame
    m = mask.copy()
    # keep only the inside of the frame
    m[: int(np.ceil(top)) + margin, :] = False
    m[int(bottom) - margin + 1:, :] = False
    m[:, : int(np.ceil(left)) + margin] = False
    m[:, int(right) - margin + 1:] = False
    for (x0, x1, y0, y1) in legend_boxes:
        m[int(y0):int(y1) + 1, int(x0):int(x1) + 1] = False
    # tick marks (inward, ~8 px long) must not be read as data
    for px in axes.xticks:
        m[int(bottom) - 16:int(bottom) + 1, int(px) - 3:int(px) + 4] = False
    for py in axes.yticks:
        m[int(py) - 3:int(py) + 4, int(left):int(left) + 17] = False
    rows = []
    for col in range(int(np.ceil(left)) + margin, int(right) - margin + 1):
        ys = np.nonzero(m[:, col])[0]
        if ys.size == 0:
            continue
        # split the column into connected clusters (gap > 4 px); isolated
        # specks (< 2 px, JPEG noise) are dropped; the median is taken on
        # the largest cluster so that stray pixels cannot bias it.
        cuts = np.nonzero(np.diff(ys) > 4)[0] + 1
        clusters = [c for c in np.split(ys, cuts) if c.size >= 2]
        if not clusters:
            continue
        main = max(clusters, key=len)
        allp = np.concatenate(clusters)
        H = axes.py2y(allp.astype(float))
        rows.append((float(axes.px2x(col)), float(np.median(axes.py2y(main.astype(float)))),
                     float(H.min()), float(H.max()), int(allp.size)))
    return rows


def run() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = {}
    for fid, cfg in FIGS.items():
        img = load_rgb(RAW / cfg["file"])
        masks = colour_masks(img)
        for pid, pc in cfg["panels"].items():
            axes = calibrate(img, pc["frame"], cfg["xticks"], cfg["yticks"],
                             cfg.get("xspine", (None, None)), cfg.get("yspine", (None, None)))
            key = f"{fid}_{pid}"
            meta[key] = {
                "frame_px": axes.frame,
                "t_per_px": axes.dx_per_px, "H_per_px": axes.dy_per_px,
                "calib_rms_t": axes.xres, "calib_rms_H": axes.yres,
                "map": {"t": [axes.ax, axes.bx], "H": [axes.ay, axes.by]},
                "series": {},
            }
            for sname, colours in cfg["series"].items():
                mask = np.zeros(img.shape[:2], bool)
                for c in colours:
                    mask |= masks[c]
                boxes = list(pc.get("legend", []))
                if "black" in colours:
                    boxes += pc.get("mask_black", [])
                rows = digitise_panel(img, axes, mask, boxes)
                path = OUT / f"{key}_{sname}.csv"
                with open(path, "w", newline="") as fh:
                    w = csv.writer(fh)
                    w.writerow(["t_s", "H_med_m", "H_min_m", "H_max_m", "npix"])
                    for r in rows:
                        w.writerow([f"{r[0]:.6f}", f"{r[1]:.3f}", f"{r[2]:.3f}", f"{r[3]:.3f}", r[4]])
                meta[key]["series"][sname] = {"colours": list(colours), "ncols": len(rows),
                                              "file": path.name}
    with open(OUT / "digitization_meta.json", "w") as fh:
        json.dump(meta, fh, indent=1)
    return meta


if __name__ == "__main__":
    m = run()
    for k, v in m.items():
        print(k, {s: d["ncols"] for s, d in v["series"].items()},
              "dt/px=%.2e dH/px=%.3f" % (v["t_per_px"], v["H_per_px"]))
