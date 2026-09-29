function V = friction_source_rk2(V, dt, f, D)
%FRICTION_SOURCE_RK2 Source step of paper Eqs. (8)-(9): explicit midpoint
%   Runge-Kutta for dV/dt = -f V|V|/(2D) (H is unaffected).
if f == 0
    return
end
k = f / (2 * D);
Vh = V - 0.5 * dt * k * V .* abs(V);
V = V - dt * k * Vh .* abs(Vh);
end
