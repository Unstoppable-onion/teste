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
