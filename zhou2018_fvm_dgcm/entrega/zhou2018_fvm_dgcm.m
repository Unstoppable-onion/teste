function res = zhou2018_fvm_dgcm(case_name, varargin)
%ZHOU2018_FVM_DGCM  Arquivo MATLAB unico (autocontido) da reproducao de
%   Zhou et al. (2018), J. Hydraul. Eng. 144(5): 04018017 - FVM-DGCM.
%
%   res = zhou2018_fvm_dgcm()                    Caso 1, Ns=32, Cr=1, C_ap=0.9, 2a ordem
%   res = zhou2018_fvm_dgcm('case3', 'Ns', 256)  outro caso / opcoes numericas
%   res = zhou2018_fvm_dgcm('case1', 'model', 'DVCM')   FVM-DVCM
%   res = zhou2018_fvm_dgcm('case1', 'solver', 'moc')   MOC-DGCM (malha escalonada)
%   res = zhou2018_fvm_dgcm('case1', 'plot', false)     sem grafico
%
%   Casos: 'case0' (teorico, sem atrito), 'case1', 'case2', 'case3' (Tabela 1).
%   Opcoes numericas: Ns, Cr, C_ap, alpha0, order (1|2), model ('DGCM'|'DVCM'),
%   collapse, limit_gas_growth, fallback (ver docs/analise_do_artigo.md).
%   Saida: res.t [s], res.H_cellN [m] (cota "na valvula"), res.H_valve, ...
%
%   Todas as funcoes do projeto (matlab/src) estao abaixo como subfuncoes;
%   nao requer toolboxes. Testado em GNU Octave 8.4 (compativel com MATLAB).
if nargin < 1 || isempty(case_name), case_name = 'case1'; end
solver = 'fvm'; do_plot = true; opts = {};
for k = 1:2:numel(varargin)
    switch varargin{k}
        case 'solver', solver = varargin{k+1};
        case 'plot',   do_plot = varargin{k+1};
        otherwise,     opts(end+1:end+2) = varargin(k:k+1); %#ok<AGROW>
    end
end
cs = case_parameters(case_name);
num = numerics_default(opts{:});
if strcmp(solver, 'moc')
    res = run_moc_dgcm(cs, num.Ns, num.alpha0);
    res.H_cellN = res.H_valve;
else
    res = run_fvm(cs, num);
end
if strcmp(case_name, 'case0') && ~strcmp(solver, 'moc')
    res.H_exact = valve_head_exact(cs, res.t);
end
if do_plot
    figure; plot(res.t, res.H_cellN, 'r-'); hold on;
    if isfield(res, 'H_exact'), plot(res.t, res.H_exact, '-', 'color', [0.6 0.6 0.6]); end
    hold off; grid on; xlabel('t (s)'); ylabel('H (m)');
    title(sprintf('%s - %s', case_name, upper(solver)));
end
end

% ==================================================================== fluid_properties
function fl = fluid_properties(varargin)
%FLUID_PROPERTIES Water and atmosphere properties (SI units).
%   fl = fluid_properties() returns water at 20 degC and the standard
%   atmosphere.  The paper (Zhou et al. 2018) does NOT report temperature,
%   vapour pressure or barometric pressure; these values are deduced
%   assumptions [DED] (docs/analise_do_artigo.md, sec. 8).
%   Name/value pairs override any field, e.g. fluid_properties('p_bar', 1e5).
fl.rho   = 998.2;      % density, kg/m^3 (20 degC)
fl.nu    = 1.004e-6;   % kinematic viscosity, m^2/s (Blasius friction)
fl.p_vap = 2339.0;     % absolute vapour pressure, Pa (20 degC)
fl.p_bar = 101325.0;   % absolute barometric pressure, Pa
fl.p0    = 101325.0;   % standard pressure of alpha0, Pa
fl.g     = 9.81;       % gravity, m/s^2
for k = 1:2:numel(varargin)
    fl.(varargin{k}) = varargin{k+1};
end
fl.Hb     = fl.p_bar / (fl.rho * fl.g);            % absolute barometric head, m
fl.Hv     = fl.p_vap / (fl.rho * fl.g) - fl.Hb;    % gauge vapour head, m (paper p. 2)
fl.H0_std = fl.p0 / (fl.rho * fl.g);               % p0*/(rho g), m
end

% ==================================================================== blasius_friction
function f = blasius_friction(V, D, nu)
%BLASIUS_FRICTION Darcy friction factor of a smooth pipe (Blasius).
%   Used because the paper does not report f [DED].
Re = abs(V) * D / nu;
f = 0.316 / Re^0.25;
end

% ==================================================================== case_parameters
function cs = case_parameters(name, varargin)
%CASE_PARAMETERS Parameters of the cases of Table 1 (Zhou et al. 2018).
%   cs = case_parameters('case1') returns a struct with (SI units):
%     V0 [m/s], Hr [m], Tc [s], D [m], L [m], a [m/s]   - Table 1 [T1]
%     rise [m]  elevation of the valve above the inlet   - text p. 4
%     K_valve   loss coefficient of the open valve        - deduced [DED]
%     t_end [s] simulated time (abscissa of the figures)
%   and derived quantities: area, friction (Darcy f), dH_valve0, joukowsky.
%   Name/value pairs override fields BEFORE the derived quantities are
%   computed, e.g. case_parameters('case1', 'f', 0.03, 'Hr', 25).
switch name
    case 'case0'
        cs = mk(0.16, 23.41, 0.0, 0.01905, 36.0, 1280.0, 0.0, true, 1.0, 2.55);
    case 'case1'
        cs = mk(0.332, 23.41, 0.022, 0.01905, 36.0, 1280.0, 1.0, false, 0.45, 2.55);
    case 'case2'
        cs = mk(1.125, 21.74, 0.024, 0.01905, 36.0, 1280.0, 1.0, false, 0.45, 2.55);
    case 'case3'
        cs = mk(0.30, 22.0, 0.009, 0.02210, 37.2, 1319.0, 37.2*sin(3.2*pi/180), false, 0.57, 18.9);
    otherwise
        error('unknown case %s', name);
end
cs.name = name;
cs.fluid = fluid_properties();
cs.f = NaN;       % NaN -> Blasius at V0
cs.z0 = 0.0;      % elevation of the inlet above the datum, m
for k = 1:2:numel(varargin)
    cs.(varargin{k}) = varargin{k+1};
end
cs.area = pi * cs.D^2 / 4;
if cs.frictionless
    cs.friction = 0.0;
elseif ~isnan(cs.f)
    cs.friction = cs.f;
else
    cs.friction = blasius_friction(cs.V0, cs.D, cs.fluid.nu);
end
cs.sin_theta = cs.rise / cs.L;
cs.dH_valve0 = cs.K_valve * cs.V0^2 / (2 * cs.fluid.g);
cs.joukowsky = cs.a * cs.V0 / cs.fluid.g;
end

function cs = mk(V0, Hr, Tc, D, L, a, rise, frictionless, t_end, K)
cs = struct('V0', V0, 'Hr', Hr, 'Tc', Tc, 'D', D, 'L', L, 'a', a, 'rise', rise, ...
            'frictionless', frictionless, 't_end', t_end, 'K_valve', K);
end

% ==================================================================== numerics_default
function num = numerics_default(varargin)
%NUMERICS_DEFAULT Numerical options of the FVM-DGCM (paper notation).
%   Ns     number of reaches (N = 2 Ns cells)
%   Cr     Courant number a dt/dx
%   C_ap   pressure-adjustment coefficient C_-ap (Eqs. 12-13)
%   alpha0 gas void fraction at standard conditions
%   order  1 (Godunov) or 2 (MUSCL-Hancock + MINMOD)
%   model  'DGCM' (this paper), 'DVCM' (Zhou et al. 2017) or 'none'
%   collapse, limit_gas_growth, fallback: interpretation choices [DED]
num.Ns = 32; num.Cr = 1.0; num.C_ap = 0.9; num.alpha0 = 1e-7; num.order = 2;
num.model = 'DGCM'; num.collapse = 'volume'; num.limit_gas_growth = true;
num.fallback = 'keep';
for k = 1:2:numel(varargin)
    num.(varargin{k}) = varargin{k+1};
end
end

% ==================================================================== pipe_elevation
function z = pipe_elevation(cs, x)
%PIPE_ELEVATION Elevation of the pipe axis (datum = pipe inlet), m.
z = cs.z0 + cs.sin_theta * x;
end

% ==================================================================== riemann_state
function [Hs, Vs] = riemann_state(HL, VL, HR, VR, a, g)
%RIEMANN_STATE Exact Riemann solution of the linear water-hammer system
%   (paper Eq. 6):  H* = (HL+HR)/2 + (a/2g)(VL-VR),
%                   V* = (VL+VR)/2 + (g/2a)(HL-HR).
%   The interface flux is f = A U* = (a^2/g V*, g H*).
Hs = 0.5 * (HL + HR) + 0.5 * (a / g) * (VL - VR);
Vs = 0.5 * (VL + VR) + 0.5 * (g / a) * (HL - HR);
end

% ==================================================================== minmod_limiter
function d = minmod_limiter(d1, d2)
%MINMOD_LIMITER Componentwise MINMOD slope limiter.
d = (d1 .* d2 > 0) .* sign(d1) .* min(abs(d1), abs(d2));
end

% ==================================================================== interface_states
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

% ==================================================================== friction_source_rk2
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

% ==================================================================== valve_tau
function tau = valve_tau(t, Tc)
%VALVE_TAU Relative valve opening, linear closure in Tc (paper p. 7).
%   Tc <= 0: instantaneous closure at t = 0.
if Tc <= 0
    tau = 0.0;
else
    tau = max(0.0, 1.0 - t / Tc);
end
end

% ==================================================================== valve_velocity
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

% ==================================================================== reservoir_state
function [HB, VB] = reservoir_state(H1, V1, Hr, a, g)
%RESERVOIR_STATE Upstream reservoir: H = Hr and C- invariant from cell I_1.
HB = Hr;
VB = V1 + (g / a) * (Hr - H1);
end

% ==================================================================== valve_state
function [HB, VB] = valve_state(HN, VN, tau, Vref, H_down, dH0, a, g)
%VALVE_STATE Downstream valve: C+ invariant from cell I_N + orifice law.
B = a / g;
Cp = HN + B * VN;
VB = valve_velocity(Cp, tau, Vref, H_down, dH0, B);
HB = Cp - B * VB;
end

% ==================================================================== valve_head_exact
function H = valve_head_exact(cs, t)
%VALVE_HEAD_EXACT Exact valve head of Case 0 (frictionless, horizontal,
%   instantaneous closure, no cavitation): square wave of period 4L/a,
%   H = Hr + aV0/g on (4k,4k+2) L/a and Hr - aV0/g on (4k+2,4k+4) L/a.
dH = cs.a * cs.V0 / cs.fluid.g;
T2 = 2 * cs.L / cs.a;
phase = mod(floor(t / T2), 2);
H = cs.Hr + dH * (1 - 2 * phase);
end

% ==================================================================== cavity_init
function st = cavity_init(Ns, zc, Hv, C3, H, num)
%CAVITY_INIT State of the Ns discrete cavities (middle of each reach).
%   zc: cavity elevations (m); Hv: gauge vapour head (m);
%   C3 = p0 alpha0 Vol_reach /(rho g) (m^4); H: initial cell heads (2 Ns).
st.Ns = Ns;
st.hvap = zc(:) + Hv;            % vapour piezometric head at each cavity, m
st.C3 = C3;
st.Vg = zeros(Ns, 1);            % cavity volume, m^3
st.cav = false(Ns, 1);           % "cavitation exists" flag
st.n_fallback = 0;
st.limit_growth = num.limit_gas_growth;
st.fallback = num.fallback;
st.Vg_init = zeros(Ns, 1);
if C3 > 0
    Hbar = 0.5 * (H(1:2:end) + H(2:2:end));
    st.Vg = C3 ./ (Hbar(:) - st.hvap);   % Eq. (11) at the initial state
    st.Vg_init = st.Vg;
end
end

% ==================================================================== apply_dgcm
function [st, H] = apply_dgcm(st, H, Q, dt, C_ap, collapse)
%APPLY_DGCM Discrete gas cavity correction of the FVM heads (paper Fig. 3).
%   Reach j = cells (2j-1, 2j) = upstream half (H_uj, Q_uj) and downstream
%   half (H_j, Q_j); the cavity lies on the interface between them.
%   Method II (cavitation at t, or a half at/below the vapour head):
%     Vg^{n+1} = Vg^n + (Q_j - Q_uj) dt                        (15)
%     Hg = p0 alpha0 Vol/(rho g Vg^{n+1}) + z(j) + Hv           (16)
%     H_uj = H_j = Hg                                           (17)
%   Method I (no cavitation at t+dt):
%     Hg = (H_uj + H_j)/2                                       (10)
%     Vg = p0 alpha0 Vol/[rho g (Hg - z(j) - Hv)]               (11)
%     H_uj <- C H_uj + (1-C) Hg ; H_j <- C H_j + (1-C) Hg       (12)-(13)
%   Interpretation choices [DED] (see docs, sec. 8.5): cavity exists at
%   t+dt while Vg^{n+1} > 0 ('volume'); continuity-limited gas growth in
%   Method I (st.limit_growth); fallback when Vg^{n+1} <= 0 with the mean
%   head at/below vapour (st.fallback).
Hu = H(1:2:end); Hd = H(2:2:end);
Qu = Q(1:2:end); Qd = Q(2:2:end);
hv = st.hvap;
Hbar = 0.5 * (Hu + Hd);

use2 = st.cav | (min(Hu, Hd) <= hv);
Vnew = st.Vg + (Qd - Qu) * dt;                 % Eq. (15)
Hg2 = st.C3 ./ Vnew + hv;                      % Eq. (16)
exists = use2 & (Vnew > 0);
if strcmp(collapse, 'pressure')
    exists = exists & ~(st.cav & (Hbar > hv) & (Hg2 > Hbar));
end

m1 = ~exists;
bad = m1 & (Hbar <= hv);
if any(bad)
    st.n_fallback = st.n_fallback + sum(bad);
    m1 = m1 & ~bad;
    if strcmp(st.fallback, 'keep')
        Hg_keep = st.C3 ./ st.Vg + hv;
        Hu(bad) = Hg_keep(bad); Hd(bad) = Hg_keep(bad);
        st.cav(bad) = true;
    else
        Hb_ = Hbar(bad);
        Hu(bad) = C_ap * Hu(bad) + (1 - C_ap) * Hb_;
        Hd(bad) = C_ap * Hd(bad) + (1 - C_ap) * Hb_;
        if strcmp(st.fallback, 'collapse')
            st.Vg(bad) = st.Vg_init(bad);
        end
        st.cav(bad) = false;
    end
end

% Method II
Hu(exists) = Hg2(exists);
Hd(exists) = Hg2(exists);
st.Vg(exists) = Vnew(exists);
st.cav(exists) = true;

% Method I
if any(m1)
    Hg1 = Hbar(m1);
    Veq = st.C3 ./ (Hg1 - hv(m1));                     % Eq. (11)
    if st.limit_growth
        Vo = st.Vg(m1);
        Veq = min(Veq, Vo + max(Vnew(m1) - Vo, 0));
    end
    st.Vg(m1) = Veq;
    Hu(m1) = C_ap * Hu(m1) + (1 - C_ap) * Hg1;         % Eq. (12)
    Hd(m1) = C_ap * Hd(m1) + (1 - C_ap) * Hg1;         % Eq. (13)
    st.cav(m1) = false;
end
H(1:2:end) = Hu; H(2:2:end) = Hd;
end

% ==================================================================== apply_dvcm
function [st, H] = apply_dvcm(st, H, Q, dt)
%APPLY_DVCM Discrete vapour cavity correction (FVM-DVCM, Zhou et al. 2017):
%   a cavity forms when a half is at/below the vapour head, its volume
%   follows continuity (Eq. 15), its head is the vapour head, and it
%   collapses (volume 0, FVM heads kept) when the volume becomes <= 0.
Hu = H(1:2:end); Hd = H(2:2:end);
Qu = Q(1:2:end); Qd = Q(2:2:end);
hv = st.hvap;
use = st.cav | (min(Hu, Hd) <= hv);
Vnew = st.Vg + (Qd - Qu) * dt;
exists = use & (Vnew > 0);
Hu(exists) = hv(exists);
Hd(exists) = hv(exists);
st.Vg = zeros(size(Vnew));
st.Vg(exists) = Vnew(exists);
st.cav = exists;
H(1:2:end) = Hu; H(2:2:end) = Hd;
end

% ==================================================================== run_fvm
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

% ==================================================================== run_moc_dgcm
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

