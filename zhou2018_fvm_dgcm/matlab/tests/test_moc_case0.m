function test_moc_case0()
cs = case_parameters('case0');
r = run_moc_dgcm(cs, 32, 1e-12);
m = away_from_fronts(cs, r.t, 0.05);
ex = valve_head_exact(cs, r.t);
check(max(abs(r.H_valve(m) - ex(m))) < 1e-3, 'MOC vs exact');
end
