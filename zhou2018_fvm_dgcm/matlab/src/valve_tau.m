function tau = valve_tau(t, Tc)
%VALVE_TAU Relative valve opening, linear closure in Tc (paper p. 7).
%   Tc <= 0: instantaneous closure at t = 0.
if Tc <= 0
    tau = 0.0;
else
    tau = max(0.0, 1.0 - t / Tc);
end
end
