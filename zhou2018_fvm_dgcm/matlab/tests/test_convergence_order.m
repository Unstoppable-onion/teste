function test_convergence_order()
% Smooth Gaussian pulse, liquid at rest, d'Alembert solution.
expected = [1.0 1.9];
for order = 1:2
    e = zeros(1, 3); Ns = [128 256 512];
    for k = 1:3, e(k) = pulse_error(Ns(k), order); end
    p = log2(e(2) / e(3));
    check(p > 0.85 * expected(order), sprintf('order %d: p = %.2f', order, p));
end
end

function err = pulse_error(Ns, order)
cs = case_parameters('case0', 'Tc', 1e9, 'V0', 0.0);
L = cs.L; a = cs.a; sig = 3.0; amp = 5.0; H0 = cs.Hr;
h0 = @(x) amp * exp(-((x - L/2) / sig).^2);
t_end = 0.25 * L / a;
r = run_fvm(cs, numerics_default('Ns', Ns, 'Cr', 0.5, 'order', order, 'model', 'none'), ...
            t_end, @(x) deal(H0 + h0(x), 0 * x));
tt = r.t(end);
Hex = H0 + 0.5 * (h0(r.x - a * tt) + h0(r.x + a * tt));
err = sqrt(mean((r.H_final - Hex).^2));
end
