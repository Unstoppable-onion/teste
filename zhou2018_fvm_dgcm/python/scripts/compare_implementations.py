"""Compare the paper-validation metrics obtained with the Python and the
MATLAB/Octave implementations (results/validation/metrics_{python,matlab}.json)
and summarise the pointwise cross-validation (cross_validation.json).

Usage: python -m scripts.compare_implementations
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VAL = ROOT / "results" / "validation"


def key(rid):
    s = "".join(c if c.isalnum() or c == "_" else "_" for c in rid)
    return s if s[0].isalpha() else "x" + s


def main():
    py = json.load(open(VAL / "metrics_python.json"))
    ml = json.load(open(VAL / "metrics_matlab.json"))
    rows, worst = [], 0.0
    for rid, e in py.items():
        a = e["vs_paper"]
        b = ml[key(rid)]
        fa, fb = a["pointwise"]["flat"]["medae"], b["pointwise"]["flat"]["medae"]
        ea = a.get("events", {}).get("mean_abs_ms", float("nan"))
        eb = b.get("events", {}).get("mean_abs_ms", float("nan"))
        d1 = abs(fa - fb)
        d2 = 0.0 if (math.isnan(ea) and (eb is None or math.isnan(eb))) else abs(ea - eb)
        worst = max(worst, d1, d2)
        rows.append((rid, a["status"], b["status"], d1, d2))
    same = sum(r[1] == r[2] for r in rows)
    print(f"{'run':16s} {'python':14s} {'matlab':14s} |d flatMedAE| m  |d evt| ms")
    for r in rows:
        print(f"{r[0]:16s} {r[1]:14s} {r[2]:14s} {r[3]:14.2e} {r[4]:10.2e}")
    cv = json.load(open(VAL / "cross_validation.json"))
    mx = max(c["max_abs_dH"] for c in cv)
    summary = dict(n_runs=len(rows), same_status=same, worst_metric_difference=worst,
                   pointwise_max_abs_dH_all_runs=mx)
    print(json.dumps(summary, indent=1))
    json.dump(summary, open(VAL / "implementations_summary.json", "w"), indent=1)


if __name__ == "__main__":
    main()
