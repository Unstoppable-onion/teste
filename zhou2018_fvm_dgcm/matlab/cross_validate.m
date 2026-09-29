function T = cross_validate()
%CROSS_VALIDATE Compare the MATLAB results (results/matlab) with the
%   validated Python results (results/python), run by run.
%   Metrics: max |dH| and RMS dH over the common time grid, relative to the
%   head range of the run, and max |dt| of the event times (crossings).
%   Tolerances (docs/relatorio_validacao.md, sec. 7):
%     smooth runs  : max |dH| <= 1e-6 m      (round-off level)
%     all runs     : event times identical within 0.05 ms, and the paper-
%                    comparison status identical to the Python one.
%   Output: results/validation/cross_validation.json and printed table.
setup_paths();
root = project_root();
runs = experiments_registry();
T = struct('id', {}, 'n', {}, 'max_abs_dH', {}, 'rms_dH', {}, 'max_evt_dt_ms', {}, 'same_n_events', {});
fprintf('%-16s %8s %12s %12s %10s\n', 'run', 'n', 'max|dH| m', 'rms dH m', 'max|dt| ms');
for k = 1:numel(runs)
    id = runs{k}.id;
    A = read_csv_numeric(fullfile(root, 'results', 'matlab', [id '.csv']));
    B = read_csv_numeric(fullfile(root, 'results', 'python', [id '.csv']));
    n = min(size(A, 1), size(B, 1));
    if max(abs(A(1:n, 1) - B(1:n, 1))) > 1e-7
        error('%s: time grids differ', id);
    end
    dH = A(1:n, 2) - B(1:n, 2);
    lev = case_features(runs{k}.case).level;
    ea = crossings_sim(A(1:n, 1), A(1:n, 2), lev);
    eb = crossings_sim(B(1:n, 1), B(1:n, 2), lev);
    same = numel(ea) == numel(eb);
    if same && ~isempty(ea)
        mdt = 1e3 * max(abs(ea - eb));
    elseif isempty(ea) && isempty(eb)
        mdt = 0;
    else
        P = pair_events(eb, ea); mdt = 1e3 * max(abs(P(:, 3)));
    end
    T(end+1) = struct('id', id, 'n', n, 'max_abs_dH', max(abs(dH)), 'rms_dH', ...
        sqrt(mean(dH .^ 2)), 'max_evt_dt_ms', mdt, 'same_n_events', same); %#ok<AGROW>
    fprintf('%-16s %8d %12.3e %12.3e %10.2e %d\n', id, n, max(abs(dH)), sqrt(mean(dH .^ 2)), mdt, same);
end
out = fullfile(root, 'results', 'validation');
if ~exist(out, 'dir'), mkdir(out); end
fid = fopen(fullfile(out, 'cross_validation.json'), 'w');
fprintf(fid, '%s', jsonencode(T));
fclose(fid);
end
