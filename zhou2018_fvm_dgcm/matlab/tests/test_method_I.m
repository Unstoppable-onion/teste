function test_method_I()
num = numerics_default('limit_gas_growth', false);   % literal Eq. (11)
st = cavity_init(4, zeros(4, 1), -10, 3e-10, zeros(8, 1) + 20, num);
H = [20 22 30 26 5 7 40 41]'; Q = zeros(8, 1); S = sum(H);
[st, H2] = apply_dgcm(st, H, Q, 1e-4, 0.5, 'volume');
Hg = 0.5 * (H(1:2:end) + H(2:2:end));
check(max(abs(st.Vg .* (Hg + 10) - 3e-10)) < 1e-20, 'Eq. (11)');
check(abs(sum(H2) - S) < 1e-12, 'Eqs. (12)-(13) conserve sum H');
end
