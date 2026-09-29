function st = cavity_init(Ns, zc, Hv, C3, H, num)
%CAVITY_INIT State of the Ns discrete cavities (middle of each reach).
%   zc: cavity elevations (m); Hv: gauge vapour head (m);
%   C3 = p0 alpha0 Vol_reach /(rho g) (m^4); H: initial cell heads (2 Ns).
st.Ns = Ns;
st.hvap = zc(:) + Hv;            % vapour piezometric head at each cavity, m
st.C3 = C3;
st.Vg = zeros(Ns, 1);            % cavity volume, m^3
st.cav = false(Ns, 1);           % "cavitation exists" flag
st.n_fallback = 0;
st.limit_growth = num.limit_gas_growth;
st.fallback = num.fallback;
st.Vg_init = zeros(Ns, 1);
if C3 > 0
    Hbar = 0.5 * (H(1:2:end) + H(2:2:end));
    st.Vg = C3 ./ (Hbar(:) - st.hvap);   % Eq. (11) at the initial state
    st.Vg_init = st.Vg;
end
end
