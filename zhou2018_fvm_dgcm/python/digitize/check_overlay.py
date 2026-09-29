"""Overlay digitised points on the original figure (visual QA of the digitisation).
Output: results/digitization_check/<fig>_<panel>.png (git-ignored: contains the
copyrighted raster)."""
from pathlib import Path
import csv, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .calibrate import load_rgb
from .figconfig import FIGS

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "digitization_check"
MARK = {0: "lime", 1: "cyan", 2: "magenta", 3: "orange"}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    meta = json.load(open(ROOT / "data/digitized/digitization_meta.json"))
    for fid, cfg in FIGS.items():
        img = load_rgb(ROOT / "data/figures_raw" / cfg["file"]).astype(np.uint8)
        for pid in cfg["panels"]:
            key = f"{fid}_{pid}"; m = meta[key]
            l, r, t, b = m["frame_px"]
            fig, ax = plt.subplots(figsize=(16, 9))
            at, bt = m["map"]["t"]; ah, bh = m["map"]["H"]
            y0, y1, x0, x1 = max(int(t) - 5, 0), int(b) + 5, max(int(l) - 5, 0), int(r) + 5
            # image drawn in data coordinates (pixel edges at k-0.5 .. k+0.5)
            ax.imshow(img[y0:y1, x0:x1], aspect="auto",
                      extent=(at * (x0 - .5) + bt, at * (x1 - .5) + bt, ah * (y1 - .5) + bh, ah * (y0 - .5) + bh))
            for k, (s, d) in enumerate(m["series"].items()):
                rows = list(csv.DictReader(open(ROOT / "data/digitized" / d["file"])))
                tt = np.array([float(x["t_s"]) for x in rows]); hh = np.array([float(x["H_med_m"]) for x in rows])
                ax.plot(tt, hh, ".", ms=2, color=MARK[k], label=s)
            ax.set_xlabel("t (s)"); ax.set_ylabel("H (m)"); ax.grid(alpha=.3)
            ax.legend(); fig.savefig(OUT / f"{key}.png", dpi=80); plt.close(fig)

if __name__ == "__main__":
    main()
