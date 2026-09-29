"""Registry of all simulations needed to reproduce Figs. 4-11 of the paper,
with the digitised series they are compared against and the comparison
windows/levels.  The MATLAB port reads the same definitions from
``results/python/run_registry.json`` (exported by scripts/run_all.py).
"""
from __future__ import annotations

# (fig, panel, run id, case, solver, numerics kwargs, digitised paper series)
RUNS: list[dict] = []


def _add(run_id, fig, case, solver, dig, **num):
    RUNS.append(dict(id=run_id, fig=fig, case=case, solver=solver, dig=dig, num=num))


# Fig. 4 - Case 0, Ns = 32, Cr = 1, first and second order, C_ap in {1, 0.9, 0.5, 0}
for p, C in zip("abcd", (1.0, 0.9, 0.5, 0.0)):
    for order in (1, 2):
        _add(f"fig04{p}_o{order}", "fig04", "case0", "fvm", f"fig04_{p}_numerical",
             Ns=32, Cr=1.0, C_ap=C, order=order, alpha0=1e-7)
    _add(f"fig04{p}_exact", "fig04", "case0", "exact", f"fig04_{p}_exact")

# Fig. 5 - Case 1, 2nd order, C_ap = 0.9, Cr = 1, Ns = 32, alpha0 in {1e-7, 1e-8, 1e-10}
for a0, tag in ((1e-7, "a1e-7"), (1e-8, "a1e-8"), (1e-10, "a1e-10")):
    _add(f"fig05_{tag}", "fig05", "case1", "fvm", f"fig05_main_{tag}",
         Ns=32, Cr=1.0, C_ap=0.9, order=2, alpha0=a0)

# Fig. 6 - Case 1, 2nd order, alpha0 = 1e-7, Cr = 1, C_ap in {1, .9, .8, .5}, Ns in {32, 256}
for p, C in zip("abcd", (1.0, 0.9, 0.8, 0.5)):
    for Ns in (32, 256):
        _add(f"fig06{p}_Ns{Ns}", "fig06", "case1", "fvm", f"fig06_{p}_Ns{Ns}",
             Ns=Ns, Cr=1.0, C_ap=C, order=2, alpha0=1e-7)

# Fig. 7 - Case 2, 2nd order, Ns = 32, C_ap in {1.0, 0.9}
for C in (1.0, 0.9):
    _add(f"fig07_Cap{C:.1f}", "fig07", "case2", "fvm", f"fig07_main_Cap{C:.1f}",
         Ns=32, Cr=1.0, C_ap=C, order=2, alpha0=1e-7)

# Fig. 8 - Case 3, 2nd order, Ns = 256, C_ap in {1.0, 0.9}
for C in (1.0, 0.9):
    _add(f"fig08_Cap{C:.1f}", "fig08", "case3", "fvm", f"fig08_main_Cap{C:.1f}",
         Ns=256, Cr=1.0, C_ap=C, order=2, alpha0=1e-7)

# Fig. 9 - Case 1, Ns = 32, C_ap = 0.9, alpha0 = 1e-7, Cr in {1, 0.5, 0.1}; (a) 1st, (b) 2nd order
for p, order in (("a", 1), ("b", 2)):
    for Cr in (1.0, 0.5, 0.1):
        _add(f"fig09{p}_Cr{Cr:.1f}", "fig09", "case1", "fvm", f"fig09_{p}_Cr{Cr:.1f}",
             Ns=32, Cr=Cr, C_ap=0.9, order=order, alpha0=1e-7)

# Fig. 10 - Case 1, second-order FVM-DVCM (Zhou et al. 2017), Ns in {32, 256}
for Ns in (32, 256):
    _add(f"fig10_Ns{Ns}", "fig10", "case1", "fvm", f"fig10_main_Ns{Ns}",
         Ns=Ns, Cr=1.0, C_ap=1.0, order=2, model="DVCM", alpha0=0.0)

# Fig. 11 - Case 1, MOC-DGCM staggered grid, Ns in {32, 256}
for Ns in (32, 256):
    _add(f"fig11_Ns{Ns}", "fig11", "case1", "moc", f"fig11_main_Ns{Ns}", Ns=Ns, alpha0=1e-7)

# Experimental records (digitised) shown in each figure
EXPERIMENT = {
    "fig05": "fig05_main_experiment", "fig06a": "fig06_a_experiment",
    "fig06b": "fig06_b_experiment", "fig06c": "fig06_c_experiment",
    "fig06d": "fig06_d_experiment", "fig07": "fig07_main_experiment",
    "fig08": "fig08_main_experiment", "fig10": "fig10_main_experiment",
    "fig11": "fig11_main_experiment",
}

# Comparison features per case: level for event timing and time windows
FEATURES = {
    "case0": dict(level=23.41, plateaus=[], peaks=[]),
    "case1": dict(level=20.0,
                  plateaus=[("H_initial", 0.002, 0.018), ("H_joukowsky", 0.03, 0.07),
                            ("H_cavity", 0.09, 0.135)],
                  peaks=[("peak_2nd_pulse", 0.17, 0.215), ("peak_3rd_pulse", 0.26, 0.33),
                         ("peak_4th_pulse", 0.37, 0.44)]),
    "case2": dict(level=80.0,
                  plateaus=[("H_initial", 0.002, 0.018), ("H_joukowsky", 0.03, 0.07),
                            ("H_cavity", 0.10, 0.29)],
                  peaks=[("peak_2nd_pulse", 0.30, 0.37)]),
    "case3": dict(level=20.0,
                  plateaus=[("H_initial", 0.001, 0.0065), ("H_joukowsky", 0.015, 0.06),
                            ("H_cavity", 0.08, 0.12)],
                  peaks=[("peak_2nd_pulse", 0.16, 0.21), ("peak_3rd_pulse", 0.25, 0.32),
                         ("peak_4th_pulse", 0.36, 0.44), ("peak_5th_pulse", 0.47, 0.55)]),
}
