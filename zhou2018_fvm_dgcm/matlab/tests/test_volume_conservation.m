function test_volume_conservation()
cs = case_parameters('case0');
for order = 1:2
    r = run_fvm(cs, numerics_default('Ns', 32, 'Cr', 0.7, 'C_ap', 1.0, 'order', order, 'model', 'none'));
    check(max(abs(r.mass_error)) / (cs.area * cs.L) < 1e-12, 'volume balance');
end
end
