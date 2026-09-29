function [Hs, Vs] = riemann_state(HL, VL, HR, VR, a, g)
%RIEMANN_STATE Exact Riemann solution of the linear water-hammer system
%   (paper Eq. 6):  H* = (HL+HR)/2 + (a/2g)(VL-VR),
%                   V* = (VL+VR)/2 + (g/2a)(HL-HR).
%   The interface flux is f = A U* = (a^2/g V*, g H*).
Hs = 0.5 * (HL + HR) + 0.5 * (a / g) * (VL - VR);
Vs = 0.5 * (VL + VR) + 0.5 * (g / a) * (HL - HR);
end
