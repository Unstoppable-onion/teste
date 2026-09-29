function [HB, VB] = valve_state(HN, VN, tau, Vref, H_down, dH0, a, g)
%VALVE_STATE Downstream valve: C+ invariant from cell I_N + orifice law.
B = a / g;
Cp = HN + B * VN;
VB = valve_velocity(Cp, tau, Vref, H_down, dH0, B);
HB = Cp - B * VB;
end
