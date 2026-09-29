function res = run_fvm(cs, num, t_end, initial)
%RUN_FVM First/second-order FVM Godunov solver with discrete cavities
%   (FVM-DGCM of Zhou et al. 2018, or FVM-DVCM) for the reservoir-pipe-valve
%   system.
%   res = run_fvm(cs, num)            simulate case struct cs (case_parameters)
%                                     with options num (numerics_default)
%   res = run_fvm(cs, num, t_end)     custom final time (s)
%   res = run_fvm(cs, num, t_end, @(x) deal(H0, V0))  custom initial state
%
%   Each time step (paper Eqs. 5-9, Fig. 3):
%     1. boundary states U_1/2 (reservoir) and U_N+1/2 (valve) at time n from
%        the Riemann invariants, copied into two virtual cells at each end;
%     2. interface states (Godunov / MUSCL-Hancock) and Riemann fluxes;
%     3. wave propagation, Eq. (7);  4. friction source (RK2), Eqs. (8)-(9);
%     5. discrete-cavity correction of each reach (DGCM or DVCM).
%   Output struct: t, H_cellN (head of the last cell = "head at the valve"
%   plotted in the paper), H_valve (boundary state), V_valve, mass_error,
%   Vg_total, meta.
fl = cs.fluid; g = fl.g; a = cs.a; D = cs.D; A = cs.area; f = cs.friction;
Ns = num.Ns; N = 2 * Ns;
dx = cs.L / N;
dt = num.Cr * dx / a;
lam = dt / dx;
if nargin < 3 || isempty(t_end), t_end = cs.t_end; end
nsteps = round(t_end / dt);

xc = ((1:N)' - 0.5) * dx;
if nargin < 4 || isempty(initial)
    Hc = cs.Hr - f * xc * cs.V0^2 / (2 * g * D);   % steady HGL
    Vc = cs.V0 * ones(N, 1);
else
    [Hc, Vc] = initial(xc);
    Hc = Hc(:); Vc = Vc(:) + 0 * Hc;
end

% valve: discrete steady state of the first-order scheme
H_valve0 = cs.Hr - f * cs.L * cs.V0^2 / (2 * g * D);
hf_cell = f * dx * cs.V0^2 / (2 * g * D);
Vref = cs.V0 + g * hf_cell / (2 * a);
dH0 = cs.dH_valve0;
H_down = H_valve0 - dH0;

% cavities at the middle of the reaches
zc = pipe_elevation(cs, (2 * (0:Ns-1)' + 1) * dx);
if strcmp(num.model, 'DGCM')
    C3 = fl.H0_std * num.alpha0 * A * 2 * dx;
else
    C3 = 0;
end
st = cavity_init(Ns, zc, fl.Hv, C3, Hc, num);

H = zeros(N + 4, 1); V = zeros(N + 4, 1);
H(3:end-2) = Hc; V(3:end-2) = Vc;

t_out = zeros(nsteps + 1, 1); Hv_out = t_out; HN_out = t_out; Vv_out = t_out;
merr = t_out; vg_out = t_out;
kst = g * A / a^2;
mass0 = kst * dx * sum(Hc) + sum(st.Vg);
net_in = 0;

for n = 0:nsteps
    t = n * dt;
    [HB0, VB0] = reservoir_state(H(3), V(3), cs.Hr, a, g);
    tau = valve_tau(t, cs.Tc);
    [HBN, VBN] = valve_state(H(end-2), V(end-2), tau, Vref, H_down, dH0, a, g);
    k = n + 1;
    t_out(k) = t; Hv_out(k) = HBN; HN_out(k) = H(end-2); Vv_out(k) = VBN;
    merr(k) = kst * dx * sum(H(3:end-2)) + sum(st.Vg) - mass0 - net_in;
    vg_out(k) = sum(st.Vg);
    if n == nsteps, break; end
    H(1:2) = HB0; V(1:2) = VB0;
    H(end-1:end) = HBN; V(end-1:end) = VBN;
    [HL, VL, HR, VR] = interface_states(H, V, a, g, lam, num.order);
    [Hs, Vs] = riemann_state(HL, VL, HR, VR, a, g);
    Hn = H(3:end-2) - lam * (a * a / g) * (Vs(2:end) - Vs(1:end-1));   % Eq. (7)
    Vn = V(3:end-2) - lam * g * (Hs(2:end) - Hs(1:end-1));
    Vn = friction_source_rk2(Vn, dt, f, D);                              % Eqs. (8)-(9)
    net_in = net_in + (Vs(1) - Vs(end)) * A * dt;
    Qn = Vn * A;
    switch num.model
        case 'DGCM'
            [st, Hn] = apply_dgcm(st, Hn, Qn, dt, num.C_ap, num.collapse);
        case 'DVCM'
            [st, Hn] = apply_dvcm(st, Hn, Qn, dt);
        case 'none'
        otherwise
            error('unknown model %s', num.model);
    end
    H(3:end-2) = Hn; V(3:end-2) = Vn;
end
res.t = t_out; res.H_valve = Hv_out; res.H_cellN = HN_out; res.V_valve = Vv_out;
res.mass_error = merr; res.Vg_total = vg_out;
res.x = xc; res.H_final = H(3:end-2); res.V_final = V(3:end-2);
res.meta = struct('case', cs.name, 'Ns', Ns, 'N', N, 'dx', dx, 'dt', dt, 'Cr', num.Cr, ...
    'C_ap', num.C_ap, 'alpha0', num.alpha0, 'order', num.order, 'model', num.model, ...
    'f', f, 'Hv', fl.Hv, 'z_valve', pipe_elevation(cs, cs.L), 'H_valve0', H_valve0, ...
    'n_fallback', st.n_fallback);
end
