function test_case0_exact_Cap1()
cs = case_parameters('case0');
for order = 1:2
    r = run_fvm(cs, numerics_default('Ns', 32, 'Cr', 1.0, 'C_ap', 1.0, 'order', order));
    ex = valve_head_exact(cs, r.t);
    m = away_from_fronts(cs, r.t);
    check(max(abs(r.H_cellN(m) - ex(m))) < 1e-9, sprintf('exact order %d', order));
end
end
