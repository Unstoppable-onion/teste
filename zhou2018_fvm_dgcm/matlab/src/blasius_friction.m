function f = blasius_friction(V, D, nu)
%BLASIUS_FRICTION Darcy friction factor of a smooth pipe (Blasius).
%   Used because the paper does not report f [DED].
Re = abs(V) * D / nu;
f = 0.316 / Re^0.25;
end
