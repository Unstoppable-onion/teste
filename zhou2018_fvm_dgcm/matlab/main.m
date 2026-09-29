%MAIN Full reproduction pipeline of Zhou et al. (2018) in MATLAB/Octave:
%   1. verification tests        (run_tests)
%   2. all simulations           (run_all)       -> results/matlab
%   3. validation vs the paper   (validate_all)  -> results/validation/metrics_matlab.json
%   4. figures                   (make_figures)  -> results/figures_matlab
%   5. cross-validation with the Python results, if present (cross_validate)
setup_paths();
assert(run_tests(), 'verification tests failed');
run_all();
validate_all();
make_figures();
if exist(fullfile(project_root(), 'results', 'python', 'fig05_a1e-7.csv'), 'file')
    cross_validate();
end
