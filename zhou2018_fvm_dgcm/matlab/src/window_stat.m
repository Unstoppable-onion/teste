function v = window_stat(t, H, t0, t1, kind, min_points)
%WINDOW_STAT Median ('median') or maximum ('max') of H on [t0, t1];
%   NaN if fewer than min_points samples (default 5).
if nargin < 6, min_points = 5; end
m = (t >= t0) & (t <= t1);
if sum(m) < min_points
    v = NaN;
elseif strcmp(kind, 'max')
    v = max(H(m));
else
    v = median(H(m));
end
end
