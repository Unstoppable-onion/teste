function test_method_II()
num = numerics_default();
st = cavity_init(1, 1.0, -10, 3e-10, [0; 0], num);
st.Vg(:) = 1e-8; st.cav(:) = true;
dt = 4e-4;
[st, H] = apply_dgcm(st, [-9.5; -9.4], [1e-5; 3e-5], dt, 0.9, 'volume');
Vnew = 1e-8 + 2e-5 * dt;
check(abs(st.Vg - Vnew) < 1e-20, 'Eq. (15)');
check(all(abs(H - (3e-10 / Vnew + 1.0 - 10.0)) < 1e-12), 'Eqs. (16)-(17)');
end
