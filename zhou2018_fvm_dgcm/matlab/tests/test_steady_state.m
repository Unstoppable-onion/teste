function test_steady_state()
cs = case_parameters('case1', 'Tc', 1e9);
r = run_fvm(cs, numerics_default('Ns', 32, 'order', 1), 0.2);
check(max(abs(r.H_cellN - r.H_cellN(1))) < 1e-3, 'steady head (1st order)');
r = run_fvm(cs, numerics_default('Ns', 32, 'order', 2), 0.2);
check(max(abs(r.H_cellN - r.H_cellN(1))) < 5e-3, 'steady head (2nd order)');
end
