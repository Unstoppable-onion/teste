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
