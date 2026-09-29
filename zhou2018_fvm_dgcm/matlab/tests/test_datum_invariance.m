function test_datum_invariance()
c1 = case_parameters('case1');
c2 = case_parameters('case1', 'Hr', c1.Hr + 7, 'z0', 7);
r1 = run_fvm(c1, numerics_default(), 0.2);
r2 = run_fvm(c2, numerics_default(), 0.2);
check(max(abs(r2.H_cellN - 7 - r1.H_cellN)) < 1e-7, 'datum invariance');
end
