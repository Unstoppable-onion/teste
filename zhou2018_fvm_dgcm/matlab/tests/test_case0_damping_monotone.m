function test_case0_damping_monotone()
cs = case_parameters('case0'); T = 4 * cs.L / cs.a;
C = [1.0 0.9 0.5 0.0]; amp = zeros(1, 4);
for k = 1:4
    r = run_fvm(cs, numerics_default('Ns', 32, 'C_ap', C(k)));
    late = r.t > 8 * T;
    amp(k) = max(r.H_cellN(late)) - min(r.H_cellN(late));
end
check(all(diff(amp) <= 1e-6), 'damping grows as C_ap decreases');
check(amp(end) < amp(1) - 1, 'C_ap = 0 damps');
end
