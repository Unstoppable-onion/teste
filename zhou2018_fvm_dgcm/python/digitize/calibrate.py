"""Axis calibration of the raster figures of Zhou et al. (2018).

For each panel the plot frame (axes box) is located by searching, near a
user-supplied approximate position, for the rows/columns with the longest
runs of dark pixels.  The inward-pointing tick marks are then detected along
the left and bottom spines, and a linear pixel->data map is fitted by least
squares through the (tick pixel, tick label) pairs.  The fit residual is a
direct measure of the calibration uncertainty and is stored with the data.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


def load_rgb(path) -> np.ndarray:
    from PIL import Image

    return np.asarray(Image.open(path).convert("RGB")).astype(np.int16)


def _longest_run(a: np.ndarray) -> int:
    best = cur = 0
    for v in a:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best


def _refine_line(dark: np.ndarray, approx: float, axis: int, span: slice, limit: int,
                 search: int = 6) -> float:
    """Centre (pixel) of a straight spine near ``approx``.

    axis=0: horizontal line (search rows); axis=1: vertical line (columns)."""
    lo, hi = max(int(approx) - search, 0), min(int(approx) + search + 1, limit)
    scores = []
    for k in range(lo, hi):
        line = dark[k, span] if axis == 0 else dark[span, k]
        scores.append(_longest_run(line))
    scores = np.array(scores)
    best = scores.max()
    idx = np.nonzero(scores >= 0.9 * best)[0] + lo
    return float(idx.mean())


def _groups(idx: np.ndarray, gap: int = 2) -> list[float]:
    if idx.size == 0:
        return []
    out, start, prev = [], idx[0], idx[0]
    for v in idx[1:]:
        if v - prev > gap:
            out.append((start + prev) / 2.0)
            start = v
        prev = v
    out.append((start + prev) / 2.0)
    return out


@dataclass
class Axes:
    """Pixel <-> data mapping of one panel."""

    frame: tuple[float, float, float, float]  # left, right, top, bottom (px)
    ax: float  # t = ax * px + bx
    bx: float
    ay: float  # H = ay * py + by
    by: float
    xres: float  # RMS residual of the x-tick fit (data units)
    yres: float
    xticks: list = field(default_factory=list)
    yticks: list = field(default_factory=list)

    def px2x(self, px):
        return self.ax * np.asarray(px) + self.bx

    def py2y(self, py):
        return self.ay * np.asarray(py) + self.by

    @property
    def dx_per_px(self) -> float:
        return abs(self.ax)

    @property
    def dy_per_px(self) -> float:
        return abs(self.ay)


def calibrate(img: np.ndarray, frame_approx, xtick_values, ytick_values,
              xspine=(None, None), yspine=(None, None),
              tick_len: int = 7, dark_thr: int = 110, tol_px: float = 3.0) -> Axes:
    """Calibrate a panel.

    ``xtick_values``/``ytick_values``: labels of the *interior* tick marks.
    ``xspine`` = (value at left spine, value at right spine) and
    ``yspine`` = (value at top spine, value at bottom spine) when the axis
    limits are known from the tick labels (None otherwise).
    Every detected tick must lie within ``tol_px`` of the position predicted
    by the others; spurious candidates (curves touching the spines) are
    rejected by choosing the subset with the smallest linear-fit residual.
    """
    dark = img.mean(axis=2) < dark_thr
    H, W = dark.shape
    l0, r0, t0, b0 = frame_approx
    hspan = slice(int(l0) + 5, int(r0) - 5)
    vspan = slice(int(t0) + 5, int(b0) - 5)
    left = _refine_line(dark, l0, 1, vspan, W)
    right = _refine_line(dark, r0, 1, vspan, W)
    top = _refine_line(dark, t0, 0, hspan, H)
    bottom = _refine_line(dark, b0, 0, hspan, H)

    # y ticks: short dark segments just right of the left spine
    c0 = int(round(left)) + 3
    band = dark[int(top) + 4:int(bottom) - 3, c0:c0 + tick_len - 2]
    rows = np.nonzero(band.sum(axis=1) >= tick_len - 3)[0] + int(top) + 4
    yt = _groups(rows)
    # x ticks: short dark segments just above the bottom spine
    r0_ = int(round(bottom)) - 3
    band = dark[r0_ - tick_len + 2:r0_, int(left) + 4:int(right) - 3]
    cols = np.nonzero(band.sum(axis=0) >= tick_len - 3)[0] + int(left) + 4
    xt = _groups(cols)

    xa = [(p, v) for p, v in zip((left, right), xspine) if v is not None]
    ya = [(p, v) for p, v in zip((top, bottom), yspine) if v is not None]
    xt = _match(xt, list(xtick_values), xa, "x", tol_px)
    yt = _match(yt, list(ytick_values), ya, "y", tol_px)
    xp = [p for p, _ in xa] + xt
    xv = [v for _, v in xa] + list(xtick_values)
    yp = [p for p, _ in ya] + yt
    yv = [v for _, v in ya] + list(ytick_values)
    ax, bx = np.polyfit(xp, xv, 1)
    ay, by = np.polyfit(yp, yv, 1)
    xres = float(np.sqrt(np.mean((ax * np.array(xp) + bx - np.array(xv)) ** 2)))
    yres = float(np.sqrt(np.mean((ay * np.array(yp) + by - np.array(yv)) ** 2)))
    return Axes((left, right, top, bottom), ax, bx, ay, by, xres, yres, list(xt), list(yt))


def _match(found, values, anchors, name, tol_px):
    """Pick, among detected candidates, the subset that (together with the
    spine anchors) is best explained by a linear map."""
    from itertools import combinations

    n = len(values)
    found = sorted(found)
    if len(found) < n:
        raise RuntimeError(f"{name}-ticks: found {found}, expected {n}")
    best, best_r = None, np.inf
    for comb in combinations(found, n):
        p = [a for a, _ in anchors] + list(comb)
        v = [b for _, b in anchors] + list(values)
        c = np.polyfit(v, p, 1)
        r = np.max(np.abs(np.polyval(c, v) - p))
        if r < best_r:
            best, best_r = list(comb), r
    if best_r > tol_px:
        raise RuntimeError(f"{name}-ticks inconsistent (max dev {best_r:.2f}px): {found}")
    return best
