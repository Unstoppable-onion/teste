function tc = crossings_sim(t, H, level)
%CROSSINGS_SIM Times at which a simulated series crosses a head level
%   (linear interpolation between samples).
s = H > level;
idx = find(s(2:end) ~= s(1:end-1));
tc = t(idx) + (level - H(idx)) ./ (H(idx+1) - H(idx)) .* (t(idx+1) - t(idx));
tc = tc(:);
end
