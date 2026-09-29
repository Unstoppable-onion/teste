function test_dvcm_collapse()
num = numerics_default('model', 'DVCM');
st = cavity_init(1, 0.0, -10, 0, [0; 0], num);
st.Vg(:) = 1e-9; st.cav(:) = true;
[st, H] = apply_dvcm(st, [5; 6], [1e-4; 0], 1e-3);
check(~st.cav && st.Vg == 0 && all(H == [5; 6]), 'DVCM collapse');
end
