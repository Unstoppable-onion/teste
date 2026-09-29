function V = validate_all()
%VALIDATE_ALL Quantitative comparison of every MATLAB run with the
%   digitised curves of the paper (same metrics/criteria as the Python
%   validation, see compare_with_digitized.m).
%   Output: results/validation/metrics_matlab.json and a printed summary.
setup_paths();
root = project_root();
runs = experiments_registry();
V = struct();
fprintf('%-16s %-14s %10s %10s\n', 'run', 'status', 'flatMedAE', 'evt ms');
for k = 1:numel(runs)
    run = runs{k};
    M = read_csv_numeric(fullfile(root, 'results', 'matlab', [run.id '.csv']));
    t = M(:, 1); H = M(:, 2);
    d = load_digitized(run.dig);
    r = compare_with_digitized(t, H, d, run.case);
    if strcmp(run.case, 'case0') && ~strcmp(run.solver, 'exact')
        cs = case_parameters('case0');
        ex = valve_head_exact(cs, t);
        T2 = 2 * cs.L / cs.a; ph = mod(t / T2, 1);
        m = (ph > 0.02) & (ph < 0.98) & (t > 0);
        r.vs_exact_max_abs_err = max(abs(H(m) - ex(m)));
    end
    V.(valid_field(run.id)) = r;
    evt = NaN;
    if isfield(r.events, 'mean_abs_ms'), evt = r.events.mean_abs_ms; end
    fprintf('%-16s %-14s %10.3f %10.3f\n', run.id, r.status, r.pointwise.flat.medae, evt);
end
out = fullfile(root, 'results', 'validation');
if ~exist(out, 'dir'), mkdir(out); end
fid = fopen(fullfile(out, 'metrics_matlab.json'), 'w');
fprintf(fid, '%s', jsonencode(V));
fclose(fid);
end
