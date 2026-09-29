function V = valve_velocity(Cp, tau, Vref, H_down, dH0, B)
%VALVE_VELOCITY Solve the orifice law V = Vref tau sqrt((H - H_down)/dH0)
%   together with the compatibility relation H = Cp - B V.
%   Cancellation-free roots; reverse flow allowed.
if tau <= 0 || Vref == 0
    V = 0.0;
    return
end
Cv2 = (Vref * tau)^2 / dH0;
dh = Cp - H_down;
if dh >= 0
    V = 2 * Cv2 * dh / (Cv2 * B + sqrt((Cv2 * B)^2 + 4 * Cv2 * dh));
else
    V = 2 * Cv2 * dh / (Cv2 * B + sqrt((Cv2 * B)^2 - 4 * Cv2 * dh));
end
end
