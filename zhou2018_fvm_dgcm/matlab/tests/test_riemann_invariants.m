function test_riemann_invariants()
a = 1280; g = 9.81;
[Hs, Vs] = riemann_state(30, 0.3, 10, -0.1, a, g);
check(abs(Hs + a/g*Vs - (30 + a/g*0.3)) < 1e-12, 'C+ invariant');
check(abs(Hs - a/g*Vs - (10 - a/g*(-0.1))) < 1e-12, 'C- invariant');
end
