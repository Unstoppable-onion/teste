"""Extract the raster figures (Figs. 4-11) embedded in Zhou et al. (2018).

The figures of the paper are stored in the PDF as JPEG images at 350 dpi.
Extracting the embedded images (instead of rendering the page) gives the
highest resolution available and avoids resampling.  The PDF itself is NOT
distributed with this project: pass its path on the command line.

Usage
-----
    python -m digitize.extract_figures /path/to/Zhou_et_al._2018.pdf

Output: ``data/figures_raw/figN.jpg`` (git-ignored, copyrighted material).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pymupdf

# (page number [1-based], order of the image on that page) -> figure id.
# Established by visual inspection of the extracted images
# (``pdfimages -list``): page 5 holds Fig. 4 (2016x1228) and Fig. 5,
# page 6 holds Figs. 6, 7, 8 and page 7 holds Figs. 9, 10, 11.
FIGURE_MAP = {
    "fig04": (5, (2016, 1228)),
    "fig05": (5, (1025, 609)),
    "fig06": (6, (1998, 1226)),
    "fig07": (6, (1026, 617)),
    "fig08": (6, (1026, 594)),
    "fig09": (7, (1026, 1247)),
    "fig10": (7, (1026, 611)),
    "fig11": (7, (1026, 610)),
}

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "figures_raw"


def extract(pdf_path: str | Path, out_dir: Path = OUT_DIR) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(str(pdf_path))
    found: dict[str, Path] = {}
    for fig_id, (page_no, size) in FIGURE_MAP.items():
        page = doc[page_no - 1]
        for img in page.get_images(full=True):
            xref, w, h = img[0], img[2], img[3]
            if (w, h) == size:
                info = doc.extract_image(xref)
                path = out_dir / f"{fig_id}.{info['ext']}"
                path.write_bytes(info["image"])
                found[fig_id] = path
                break
        if fig_id not in found:
            raise RuntimeError(f"{fig_id}: image {size} not found on page {page_no}")
    return found


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    for k, v in extract(sys.argv[1]).items():
        print(k, "->", v)
