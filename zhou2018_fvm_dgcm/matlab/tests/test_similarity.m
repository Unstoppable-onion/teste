function test_similarity()
c1 = case_parameters('case0');
c2 = case_parameters('case0', 'L', 72, 'a', 2560, 'V0', 0.08);
r1 = run_fvm(c1, numerics_default('C_ap', 0.5), 0.3);
r2 = run_fvm(c2, numerics_default('C_ap', 0.5), 0.3);
check(max(abs(r1.H_cellN - r2.H_cellN)) < 1e-9, 'H depends on L/a only');
end
