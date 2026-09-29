function ok = run_tests()
%RUN_TESTS Verification tests of the MATLAB port (same checks as the
%   Python pytest suite, python/tests/test_solver.py).
%   Returns true if all tests pass; prints a report.
setup_paths();
tests = {@test_riemann_invariants, @test_case0_exact_Cap1, @test_case0_damping_monotone, ...
         @test_steady_state, @test_volume_conservation, @test_convergence_order, ...
         @test_method_I, @test_method_II, @test_dvcm_collapse, @test_valve_law, ...
         @test_moc_case0, @test_moc_steady, @test_similarity, @test_datum_invariance, ...
         @test_vapour_head};
ok = true;
for k = 1:numel(tests)
    name = func2str(tests{k});
    try
        tests{k}();
        fprintf('PASS  %s\n', name);
    catch err
        ok = false;
        fprintf('FAIL  %s : %s\n', name, err.message);
    end
end
if ok, fprintf('All %d tests passed.\n', numel(tests)); end
end
