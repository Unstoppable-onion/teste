function res = run_moc_dgcm(cs, Ns, alpha0, psi, t_end)
%RUN_MOC_DGCM Classic MOC discrete gas cavity model on a staggered grid
%   (Wylie 1984; Wylie et al. 1993), reference model of the paper's Fig. 11.
%   Nodes i = 0..Ns (index i+1 here), dx = L/Ns, dt = dx/a; at step k only
%   the nodes with (i + k) even are computed (each node every 2 dt).
%     C+ : H_P = C_P - B Q_Pu,  C_P = H_A + B Q_A - R Q_A|Q_A|
%     C- : H_P = C_M + B Q_P,   C_M = H_B - B Q_B + R Q_B|Q_B|
%     Vg_P (H_P - z - Hv) = C3,
%     Vg_P = Vg_old + dt_i [psi (Q_P - Q_Pu) + (1-psi)(Q - Q_u)_old]
%   -> quadratic in y = H_P - z - Hv (positive root).  B = a/(gA),
%   R = f dx/(2 g D A^2).  Interior nodes of the same parity are
%   independent and are computed in vectorised form.
if nargin < 2 || isempty(Ns), Ns = 32; end
if nargin < 3 || isempty(alpha0), alpha0 = 1e-7; end
if nargin < 4 || isempty(psi), psi = 1.0; end
if nargin < 5 || isempty(t_end), t_end = cs.t_end; end
if mod(Ns, 2) ~= 0, error('staggered grid requires an even Ns'); end
fl = cs.fluid; g = fl.g; a = cs.a; D = cs.D; A = cs.area; f = cs.friction;
dx = cs.L / Ns; dt = dx / a; nsteps = round(t_end / dt);
B = a / (g * A); R = f * dx / (2 * g * D * A * A);
x = (0:Ns)' * dx;
zhv = pipe_elevation(cs, x) + fl.Hv;
C3 = fl.H0_std * alpha0 * A * dx;
Q0 = cs.V0 * A;
H = cs.Hr - f * x * cs.V0^2 / (2 * g * D);
Q = Q0 * ones(Ns + 1, 1); Qu = Q;
Vg = C3 ./ (H - zhv); Vg(1) = 0;
t_last = zeros(Ns + 1, 1);
H_valve0 = H(end); dH0 = cs.dH_valve0; H_down = H_valve0 - dH0;

nout = floor(nsteps / 2) + 1;
t_out = zeros(nout, 1); h_out = zeros(nout, 1);
t_out(1) = 0; h_out(1) = H(end); ko = 1;
for k = 1:nsteps
    t = k * dt;
    Hn = H; Qn = Q; Qun = Qu;
    par = mod(k, 2);
    % ---- interior nodes of this parity (0-based i, 1 <= i <= Ns-1)
    if par == 1, i0 = 1:2:(Ns - 1); else, i0 = 2:2:(Ns - 1); end
    j = i0 + 1;                        % 1-based index
    dti = t - t_last(j);
    CP = H(j-1) + B * Q(j-1) - R * Q(j-1) .* abs(Q(j-1));
    CM = H(j+1) - B * Qu(j+1) + R * Qu(j+1) .* abs(Qu(j+1));
    K1 = 2 * psi * dti / B;
    K0 = Vg(j) + dti .* (psi * (2 * zhv(j) - CP - CM) / B + (1 - psi) * (Q(j) - Qu(j)));
    y = gas_root(K1, K0, C3);
    Hn(j) = y + zhv(j);
    Vg(j) = C3 ./ y;
    Qn(j) = (Hn(j) - CM) / B;
    Qun(j) = (CP - Hn(j)) / B;
    t_last(j) = t;
    if par == 0
        % ---- upstream reservoir (node 0)
        CM0 = H(2) - B * Qu(2) + R * Qu(2) * abs(Qu(2));
        Hn(1) = cs.Hr; Qn(1) = (cs.Hr - CM0) / B; Qun(1) = Qn(1);
        t_last(1) = t;
        % ---- valve node (Ns) with gas cavity
        jv = Ns + 1;
        dtv = t - t_last(jv);
        CPv = H(jv-1) + B * Q(jv-1) - R * Q(jv-1) * abs(Q(jv-1));
        tau = valve_tau(t, cs.Tc);
        if tau > 0
            Qv = A * valve_velocity(CPv, tau, cs.V0, H_down, dH0, B * A);
            Hn(jv) = CPv - B * Qv;
            Qn(jv) = Qv; Qun(jv) = Qv;
            Vg(jv) = C3 / max(Hn(jv) - zhv(jv), 1e-12);
        else
            Qv = 0;
            K1v = psi * dtv / B;
            K0v = Vg(jv) + dtv * (psi * (Qv - (CPv - zhv(jv)) / B) + (1 - psi) * (Q(jv) - Qu(jv)));
            yv = gas_root(K1v, K0v, C3);
            Hn(jv) = yv + zhv(jv);
            Vg(jv) = C3 / yv;
            Qn(jv) = Qv;
            Qun(jv) = (CPv - Hn(jv)) / B;
        end
        t_last(jv) = t;
    end
    H = Hn; Q = Qn; Qu = Qun;
    if par == 0
        ko = ko + 1;
        t_out(ko) = t; h_out(ko) = H(end);
    end
end
res.t = t_out(1:ko); res.H_valve = h_out(1:ko);
res.meta = struct('case', cs.name, 'Ns', Ns, 'dx', dx, 'dt', dt, 'psi', psi, ...
                  'alpha0', alpha0, 'f', f);
end

function y = gas_root(K1, K0, C3)
% positive root of K1 y^2 + K0 y - C3 = 0 (numerically stable form)
disc = sqrt(K0 .^ 2 + 4 * K1 .* C3);
y = zeros(size(K0));
p = K0 >= 0;
y(p) = 2 * C3 ./ (K0(p) + disc(p));
y(~p) = (-K0(~p) + disc(~p)) ./ (2 * K1(~p));
end
