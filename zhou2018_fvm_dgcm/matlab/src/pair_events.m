function P = pair_events(t_ref, t_sim, max_dt)
%PAIR_EVENTS One-to-one pairing of event times: candidate pairs closer than
%   max_dt (default 10 ms) are accepted greedily by increasing |dt|, each
%   event being used at most once.  Rows [t_ref t_sim dt], sorted by t_ref.
if nargin < 3, max_dt = 0.01; end
P = zeros(0, 3);
if isempty(t_sim) || isempty(t_ref), return; end
[I, J] = ndgrid(1:numel(t_ref), 1:numel(t_sim));
D = abs(t_sim(J) - t_ref(I));
D = D(:); I = I(:); J = J(:);
keep = D <= max_dt;
D = D(keep); I = I(keep); J = J(keep);
[~, o] = sort(D);
used_r = false(numel(t_ref), 1); used_s = false(numel(t_sim), 1);
for k = o(:)'
    if used_r(I(k)) || used_s(J(k)), continue; end
    used_r(I(k)) = true; used_s(J(k)) = true;
    P(end+1, :) = [t_ref(I(k)), t_sim(J(k)), t_sim(J(k)) - t_ref(I(k))]; %#ok<AGROW>
end
P = sortrows(P, 1);
end
