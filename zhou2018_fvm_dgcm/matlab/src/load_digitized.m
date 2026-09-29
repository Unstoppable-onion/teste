function d = load_digitized(key)
%LOAD_DIGITIZED Digitised paper series data/digitized/<key>.csv
%   Fields: t, H (column median), Hmin, Hmax (pixel extent), dt_px, dH_px
%   (resolution, s/px and m/px), coverage (fraction of the time axis where
%   the series is visible).
root = project_root();
M = read_csv_numeric(fullfile(root, 'data', 'digitized', [key '.csv']));
d.t = M(:, 1); d.H = M(:, 2); d.Hmin = M(:, 3); d.Hmax = M(:, 4);
meta = jsondecode(fileread(fullfile(root, 'data', 'digitized', 'digitization_meta.json')));
parts = strsplit(key, '_');
fp = [parts{1} '_' parts{2}];
m = meta.(fp);
d.dt_px = m.t_per_px; d.dH_px = m.H_per_px; d.calib_rms_H = m.calib_rms_H;
d.coverage = numel(d.t) / max(m.frame_px(2) - m.frame_px(1) - 6, 1);
end
