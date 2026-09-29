function test_moc_steady()
cs = case_parameters('case1', 'Tc', 1e9);
r = run_moc_dgcm(cs, 32, 1e-7, 1.0, 0.1);
check(max(abs(r.H_valve - r.H_valve(1))) < 1e-6, 'MOC steady state');
end
