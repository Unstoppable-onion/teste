function test_valve_law()
B = 1280 / 9.81; Vref = 0.332; Hd = 23.0; dH0 = 0.014;
cases = [40 0.5; 23.1 1.0; 10 0.3; 60 0.01];
for k = 1:size(cases, 1)
    Cp = cases(k, 1); tau = cases(k, 2);
    V = valve_velocity(Cp, tau, Vref, Hd, dH0, B);
    H = Cp - B * V;
    res = V * abs(V) * dH0 / (Vref * tau)^2 - (H - Hd);
    check(abs(res) < 1e-11 * max(1, abs(Cp)), 'orifice law residual');
end
end
