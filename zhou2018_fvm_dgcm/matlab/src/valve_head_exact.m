function H = valve_head_exact(cs, t)
%VALVE_HEAD_EXACT Exact valve head of Case 0 (frictionless, horizontal,
%   instantaneous closure, no cavitation): square wave of period 4L/a,
%   H = Hr + aV0/g on (4k,4k+2) L/a and Hr - aV0/g on (4k+2,4k+4) L/a.
dH = cs.a * cs.V0 / cs.fluid.g;
T2 = 2 * cs.L / cs.a;
phase = mod(floor(t / T2), 2);
H = cs.Hr + dH * (1 - 2 * phase);
end
