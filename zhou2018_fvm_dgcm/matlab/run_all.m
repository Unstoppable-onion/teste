function run_all(only)
%RUN_ALL Run every simulation of the reproduction matrix (Figs. 4-11).
%   run_all()          all runs
%   run_all('fig06')   only the runs whose id starts with 'fig06'
%   Output: results/matlab/<run id>.csv  (t_s, H_m[, H_boundary_m])
%           results/matlab/runs_meta.json
if nargin < 1, only = ''; end
setup_paths();
out = fullfile(project_root(), 'results', 'matlab');
if ~exist(out, 'dir'), mkdir(out); end
runs = experiments_registry();
meta = struct();
for k = 1:numel(runs)
    run = runs{k};
    if ~isempty(only) && ~strncmp(run.id, only, numel(only)), continue; end
    tic;
    [t, H, Hb, m] = simulate_run(run);
    m.cpu_s = toc;
    write_run_csv(fullfile(out, [run.id '.csv']), t, H, Hb);
    meta.(valid_field(run.id)) = m;
    fprintf('%-18s %7.2f s\n', run.id, m.cpu_s);
end
fid = fopen(fullfile(out, 'runs_meta.json'), 'w');
fprintf(fid, '%s', jsonencode(meta));
fclose(fid);
end

function write_run_csv(file, t, H, Hb)
fid = fopen(file, 'w');
if isempty(Hb)
    fprintf(fid, 't_s,H_m\n');
    fprintf(fid, '%.8f,%.9f\n', [t(:)'; H(:)']);
else
    fprintf(fid, 't_s,H_m,H_boundary_m\n');
    fprintf(fid, '%.8f,%.9f,%.9f\n', [t(:)'; H(:)'; Hb(:)']);
end
fclose(fid);
end
