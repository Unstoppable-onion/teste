function res = compare_with_digitized(t, H, d, case_name, tol_px)
%COMPARE_WITH_DIGITIZED Metrics and acceptance criteria of a simulated
%   series against a digitised series (same rules as python/scripts/validate.py):
%   T_FLAT  median |dH| on flat parts <= 3 px
%   T_PLAT  |dH| of plateau heads      <= 3 px
%   T_EVT1  |dt| of the first 2 events <= 1.5 ms
%   T_EVT   mean |dt| of all events    <= 2.5 ms
%   T_EVTN  fraction of paper events paired >= 75 %
%   T_PEAK  |dH| of pulse peaks        <= max(5 m, 10 % of the peak)
%   status: VALIDADO | PARCIAL (only T_PEAK fails) | DIVERGENTE |
%           NAO_AVALIAVEL (series visible in < 20 % of the axis)
if nargin < 5, tol_px = 3.0; end
ft = case_features(case_name);
res.pointwise = pointwise_errors(t, H, d);
crit = struct();
px = d.dH_px;
crit.T_FLAT = res.pointwise.flat.medae <= tol_px * px;
res.plateaus = struct();
okp = true; anyp = false;
for k = 1:size(ft.plateaus, 1)
    p = window_stat(d.t, d.H, ft.plateaus{k, 2}, ft.plateaus{k, 3}, 'median');
    s = window_stat(t, H, ft.plateaus{k, 2}, ft.plateaus{k, 3}, 'median');
    res.plateaus.(ft.plateaus{k, 1}) = struct('paper', p, 'sim', s, 'diff', s - p);
    if ~isnan(p), anyp = true; okp = okp && abs(s - p) <= tol_px * px; end
end
if size(ft.plateaus, 1) > 0, crit.T_PLAT = okp || ~anyp; end
res.peaks = struct();
okk = true;
for k = 1:size(ft.peaks, 1)
    p = window_stat(d.t, d.Hmax, ft.peaks{k, 2}, ft.peaks{k, 3}, 'max');
    s = window_stat(t, H, ft.peaks{k, 2}, ft.peaks{k, 3}, 'max');
    tol = max(5.0, 0.10 * abs(p));
    res.peaks.(ft.peaks{k, 1}) = struct('paper', p, 'sim', s, 'diff', s - p, 'tol', tol);
    if ~isnan(p), okk = okk && abs(s - p) <= tol; end
end
if size(ft.peaks, 1) > 0, crit.T_PEAK = okk; end
ev_p = crossings_dig(d, ft.level);
ev_s = crossings_sim(t, H, ft.level);
P = pair_events(ev_p, ev_s);
res.events = struct('level', ft.level, 'paper', ev_p, 'sim', ev_s, 'pairs', P);
if ~isempty(P)
    res.events.mean_abs_ms = 1e3 * mean(abs(P(:, 3)));
    res.events.first2_max_abs_ms = 1e3 * max(abs(P(1:min(2, end), 3)));
    crit.T_EVT1 = res.events.first2_max_abs_ms <= 1.5;
    crit.T_EVT = res.events.mean_abs_ms <= 2.5;
end
if ~isempty(ev_p)
    % at least 75 % of the paper's events must have a counterpart within 10 ms
    res.events.paired_fraction = size(P, 1) / numel(ev_p);
    crit.T_EVTN = res.events.paired_fraction >= 0.75;
end
res.criteria = crit;
res.coverage = d.coverage;
names = fieldnames(crit);
bulk = true;
for k = 1:numel(names)
    if ~strcmp(names{k}, 'T_PEAK'), bulk = bulk && crit.(names{k}); end
end
if d.coverage < 0.2
    res.status = 'NAO_AVALIAVEL';
elseif ~bulk
    res.status = 'DIVERGENTE';
elseif isfield(crit, 'T_PEAK') && ~crit.T_PEAK
    res.status = 'PARCIAL';
else
    res.status = 'VALIDADO';
end
end
