function m = away_from_fronts(cs, t, margin)
if nargin < 3, margin = 0.02; end
T2 = 2 * cs.L / cs.a;
ph = mod(t / T2, 1);
m = (ph > margin) & (ph < 1 - margin) & (t > 0);
end
