"""Per-figure digitisation configuration (panels, tick labels, series, masks).

All pixel coordinates refer to the images produced by ``extract_figures``.
Frames are approximate (refined automatically); legend masks were drawn by
visual inspection so that legend lines/text are not mistaken for data.
Series colours follow the legends of the paper.
"""

# tick labels (interior ticks only)
X01 = [0.1, 0.2, 0.3, 0.4]
Y_H140 = [140, 100, 60, 20]

FIGS = {
    "fig04": {
        "file": "fig04.jpeg",
        "panels": {
            # Case 0, Ns=32, Cr=1; exact (grey), 2nd (red dots), 1st (blue)
            "a": {"frame": (119.5, 966.5, 17.5, 485.5), "legend": [(600, 966, 17, 125)],
                  "C_ap": 1.0},
            "b": {"frame": (1159.0, 2006.5, 17.5, 485.5), "legend": [(1640, 2006, 17, 130)],
                  "C_ap": 0.9},
            "c": {"frame": (119.5, 966.5, 648.5, 1116.5), "legend": [(600, 966, 648, 752)],
                  "C_ap": 0.5},
            "d": {"frame": (1159.0, 2006.5, 648.5, 1116.5), "legend": [(1640, 2006, 648, 762)],
                  "C_ap": 0.0},
        },
        "xticks": [0.2, 0.4, 0.6, 0.8], "xspine": (0.0, 1.0),
        "yticks": [40, 20], "yspine": (60.0, 0.0),
        "series": {"numerical": ("red", "blue"), "exact": ("grey",)},
    },
    "fig05": {
        "file": "fig05.jpeg",
        "panels": {"main": {"frame": (125.5, 1019.5, 3.5, 497.5),
                            "legend": [(495, 1019, 3, 60), (535, 1019, 60, 200),
                                       (490, 540, 55, 82), (490, 540, 110, 135),
                                       (490, 540, 140, 160), (490, 540, 163, 180)]}},
        "xticks": X01, "yticks": Y_H140, "xspine": (0.0, 0.45), "yspine": (160.0, -20.0),
        "series": {"experiment": ("black",), "a1e-10": ("grey",), "a1e-8": ("red",),
                   "a1e-7": ("blue",)},
    },
    "fig06": {
        "file": "fig06.jpeg",
        "panels": {
            "a": {"frame": (123.5, 970.5, 3.5, 470.5), "legend": [(515, 970, 3, 130)], "C_ap": 1.0},
            "b": {"frame": (1146.5, 1992.5, 3.5, 470.5), "legend": [(1540, 1992, 3, 130)], "C_ap": 0.9},
            "c": {"frame": (123.5, 970.5, 650.5, 1118.0), "legend": [(515, 970, 650, 780)], "C_ap": 0.8},
            "d": {"frame": (1146.5, 1992.5, 650.5, 1118.0), "legend": [(1540, 1992, 650, 780)], "C_ap": 0.5},
        },
        "xticks": X01, "yticks": Y_H140, "xspine": (0.0, 0.45), "yspine": (160.0, -20.0),
        "series": {"experiment": ("black",), "Ns256": ("grey",), "Ns32": ("red",)},
    },
    "fig07": {
        "file": "fig07.jpeg",
        "panels": {"main": {"frame": (125.5, 1020.5, 17.5, 507.5),
                            # legend sample lines (all series) ...
                            "legend": [(355, 405, 38, 64), (355, 405, 86, 114), (355, 405, 136, 164)],
                            # ... and legend text (black only: it touches the 2nd pulse)
                            "mask_black": [(405, 1020, 33, 150), (405, 700, 150, 166)]}},
        "xticks": X01, "yticks": [180, 130, 80, 30], "xspine": (0.0, 0.45), "yspine": (230.0, -20.0),
        "series": {"experiment": ("black",), "Cap1.0": ("grey",), "Cap0.9": ("red",)},
    },
    "fig08": {
        "file": "fig08.jpeg",
        "panels": {"main": {"frame": (130.5, 1020.5, 3.5, 488.5),
                            "legend": [(495, 1020, 3, 60), (560, 1020, 60, 150),
                                       (490, 572, 55, 104), (490, 572, 120, 146)]}},
        "xticks": [0.1, 0.2, 0.3, 0.4, 0.5], "yticks": [130, 100, 70, 40, 10],
        "xspine": (0.0, None), "yspine": (None, -20.0),
        "series": {"experiment": ("black",), "Cap1.0": ("grey",), "Cap0.9": ("red",)},
    },
    "fig09": {
        "file": "fig09.jpeg",
        "panels": {
            "a": {"frame": (134.5, 1020.5, 3.5, 493.5), "legend": [(540, 1020, 3, 195)], "order": 1},
            "b": {"frame": (134.5, 1020.5, 644.5, 1134.5), "legend": [(540, 1020, 644, 836)], "order": 2},
        },
        "xticks": X01, "yticks": Y_H140, "xspine": (0.0, 0.45), "yspine": (160.0, -20.0),
        # in Fig. 9 the black curve is a *numerical* result (Cr = 1.0)
        "series": {"Cr1.0": ("black",), "Cr0.5": ("red",), "Cr0.1": ("blue",)},
    },
    "fig10": {
        "file": "fig10.jpeg",
        "panels": {"main": {"frame": (121.5, 1020.5, 3.5, 500.5),
                            "legend": [(125, 290, 3, 80), (540, 1020, 3, 60), (600, 1020, 60, 170),
                                       (540, 600, 60, 105), (540, 600, 130, 150)]}},
        "xticks": X01, "yticks": Y_H140, "xspine": (0.0, 0.45), "yspine": (160.0, -20.0),
        "series": {"experiment": ("black",), "Ns256": ("grey",), "Ns32": ("red",)},
    },
    "fig11": {
        "file": "fig11.jpeg",
        "panels": {"main": {"frame": (123.5, 1020.5, 3.5, 498.5),
                            "legend": [(125, 290, 3, 80), (570, 1020, 3, 60), (610, 1020, 60, 160),
                                       (570, 610, 60, 105), (570, 610, 128, 150)]}},
        "xticks": X01, "yticks": Y_H140, "xspine": (0.0, 0.45), "yspine": (160.0, -20.0),
        "series": {"experiment": ("black",), "Ns256": ("grey",), "Ns32": ("red",)},
    },
}
