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
