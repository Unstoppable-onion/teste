function d = minmod_limiter(d1, d2)
%MINMOD_LIMITER Componentwise MINMOD slope limiter.
d = (d1 .* d2 > 0) .* sign(d1) .* min(abs(d1), abs(d2));
end
