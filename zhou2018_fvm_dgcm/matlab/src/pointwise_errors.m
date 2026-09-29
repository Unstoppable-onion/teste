function out = pointwise_errors(t_sim, H_sim, d, flat_px)
%POINTWISE_ERRORS Errors of a simulation at the digitised abscissae:
%   'all' columns and 'flat' columns (vertical pixel extent <= flat_px px;
%   at vertical fronts a sub-ms time shift gives arbitrary head errors).
if nargin < 4, flat_px = 4.0; end
Hs = interp1(t_sim, H_sim, min(max(d.t, t_sim(1)), t_sim(end)));  % clamp as numpy.interp
sel = true(size(d.t));
flat = (d.Hmax - d.Hmin) <= flat_px * d.dH_px;
out.all = stats(Hs(sel) - d.H(sel));
out.flat = stats(Hs(flat) - d.H(flat));
end

function s = stats(e)
s.n = numel(e); s.rmse = sqrt(mean(e .^ 2)); s.mae = mean(abs(e));
s.medae = median(abs(e)); s.maxae = max(abs(e)); s.bias = mean(e);
end
