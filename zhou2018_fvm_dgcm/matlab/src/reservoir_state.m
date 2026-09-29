function [HB, VB] = reservoir_state(H1, V1, Hr, a, g)
%RESERVOIR_STATE Upstream reservoir: H = Hr and C- invariant from cell I_1.
HB = Hr;
VB = V1 + (g / a) * (Hr - H1);
end
