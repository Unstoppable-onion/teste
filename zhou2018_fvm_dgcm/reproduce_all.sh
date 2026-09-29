#!/usr/bin/env bash
# Full reproduction pipeline (Python reference + MATLAB/Octave port).
# Usage: ./reproduce_all.sh [path/to/Zhou_et_al._2018.pdf]
# The PDF is only needed to (re)digitise the figures; the digitised data are
# already in data/digitized/.
set -euo pipefail
cd "$(dirname "$0")/python"
if [ $# -ge 1 ]; then
    python3 -m digitize.extract_figures "$1"
    python3 -m digitize.extract_curves
    python3 -m digitize.check_overlay
fi
python3 -m pytest -q tests
python3 -m scripts.calibrate_valve
python3 -m scripts.run_all
python3 -m scripts.validate
python3 -m scripts.verify_claims
python3 -m scripts.sensitivity
python3 -m scripts.roundoff_sensitivity
python3 -m scripts.make_figures
if command -v octave >/dev/null 2>&1; then
    (cd ../matlab && octave --no-gui --eval "setup_paths; assert(run_tests()); run_all; validate_all; cross_validate;")
    python3 -m scripts.compare_implementations
    python3 -m scripts.make_figures --sim-dir ../results/matlab --out ../results/figures_matlab
elif command -v matlab >/dev/null 2>&1; then
    (cd ../matlab && matlab -batch "main")
    python3 -m scripts.compare_implementations
fi
python3 -m scripts.report_tables
