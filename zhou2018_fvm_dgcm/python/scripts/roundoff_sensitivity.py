"""Sensitivity of the solutions to round-off-level perturbations.

A relative perturbation of 1e-13 is applied to the reservoir head Hr and the
maximum/RMS difference of the valve head is recorded.  Runs with
C_ap = 1 (spiky, ill-conditioned) amplify such perturbations to O(100 m)
spikes, which bounds what any pointwise comparison of spikes (with the
paper or between implementations) can mean.

Output: results/validation/roundoff_sensitivity.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from fvmdgcm.fvm_solver import run_fvm
from fvmdgcm.params import CASES, Numerics

ROOT = Path(__file__).resolve().parents[2]


def main():
    out = {}
    for cname, Ns, C in (("case1", 32, 1.0), ("case1", 32, 0.9), ("case1", 256, 1.0),
                         ("case1", 256, 0.9), ("case3", 256, 1.0), ("case3", 256, 0.9)):
        c = CASES[cname]
        r0 = run_fvm(c, Numerics(Ns=Ns, C_ap=C))
        r1 = run_fvm(c.with_(Hr=c.Hr * (1 + 1e-13)), Numerics(Ns=Ns, C_ap=C))
        d = np.abs(r0.H_cellN - r1.H_cellN)
        k = f"{cname}_Ns{Ns}_Cap{C}"
        out[k] = dict(max_abs_dH=float(d.max()), rms_dH=float(np.sqrt(np.mean(d ** 2))),
                      first_time_dH_gt_1mm=float(r0.t[np.argmax(d > 1e-3)]) if (d > 1e-3).any() else None)
        print(k, out[k])
    json.dump(out, open(ROOT / "results" / "validation" / "roundoff_sensitivity.json", "w"), indent=1)


if __name__ == "__main__":
    main()
