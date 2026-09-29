function [HL, VL, HR, VR] = interface_states(H, V, a, g, lam, order)
%INTERFACE_STATES Left/right states at the N+1 cell interfaces.
%   H, V: extended column vectors of length N+4 (two virtual cells on each
%   side: I_-1, I_0, I_1..I_N, I_N+1, I_N+2).  lam = dt/dx.
%   order 1: piecewise constant (Godunov).
%   order 2: MUSCL-Hancock (Toro 2009) with MINMOD slopes; boundary values
%            evolved by dt/2 with the source-free flux (source by splitting,
%            paper Eqs. 7-9).
if order == 1
    HL = H(2:end-2); VL = V(2:end-2);
    HR = H(3:end-1); VR = V(3:end-1);
    return
end
dH = minmod_limiter(H(2:end-1) - H(1:end-2), H(3:end) - H(2:end-1));
dV = minmod_limiter(V(2:end-1) - V(1:end-2), V(3:end) - V(2:end-1));
Hc = H(2:end-1); Vc = V(2:end-1);
cH = 0.5 * lam * (a * a / g) * dV;      % (lam/2) (A dU)_H
cV = 0.5 * lam * g * dH;                % (lam/2) (A dU)_V
HmL = Hc - 0.5 * dH - cH;  VmL = Vc - 0.5 * dV - cV;   % evolved left values
HmR = Hc + 0.5 * dH - cH;  VmR = Vc + 0.5 * dV - cV;   % evolved right values
HL = HmR(1:end-1); VL = VmR(1:end-1);
HR = HmL(2:end);   VR = VmL(2:end);
end
