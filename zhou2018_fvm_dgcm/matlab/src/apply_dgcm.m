function [st, H] = apply_dgcm(st, H, Q, dt, C_ap, collapse)
%APPLY_DGCM Discrete gas cavity correction of the FVM heads (paper Fig. 3).
%   Reach j = cells (2j-1, 2j) = upstream half (H_uj, Q_uj) and downstream
%   half (H_j, Q_j); the cavity lies on the interface between them.
%   Method II (cavitation at t, or a half at/below the vapour head):
%     Vg^{n+1} = Vg^n + (Q_j - Q_uj) dt                        (15)
%     Hg = p0 alpha0 Vol/(rho g Vg^{n+1}) + z(j) + Hv           (16)
%     H_uj = H_j = Hg                                           (17)
%   Method I (no cavitation at t+dt):
%     Hg = (H_uj + H_j)/2                                       (10)
%     Vg = p0 alpha0 Vol/[rho g (Hg - z(j) - Hv)]               (11)
%     H_uj <- C H_uj + (1-C) Hg ; H_j <- C H_j + (1-C) Hg       (12)-(13)
%   Interpretation choices [DED] (see docs, sec. 8.5): cavity exists at
%   t+dt while Vg^{n+1} > 0 ('volume'); continuity-limited gas growth in
%   Method I (st.limit_growth); fallback when Vg^{n+1} <= 0 with the mean
%   head at/below vapour (st.fallback).
Hu = H(1:2:end); Hd = H(2:2:end);
Qu = Q(1:2:end); Qd = Q(2:2:end);
hv = st.hvap;
Hbar = 0.5 * (Hu + Hd);

use2 = st.cav | (min(Hu, Hd) <= hv);
Vnew = st.Vg + (Qd - Qu) * dt;                 % Eq. (15)
Hg2 = st.C3 ./ Vnew + hv;                      % Eq. (16)
exists = use2 & (Vnew > 0);
if strcmp(collapse, 'pressure')
    exists = exists & ~(st.cav & (Hbar > hv) & (Hg2 > Hbar));
end

m1 = ~exists;
bad = m1 & (Hbar <= hv);
if any(bad)
    st.n_fallback = st.n_fallback + sum(bad);
    m1 = m1 & ~bad;
    if strcmp(st.fallback, 'keep')
        Hg_keep = st.C3 ./ st.Vg + hv;
        Hu(bad) = Hg_keep(bad); Hd(bad) = Hg_keep(bad);
        st.cav(bad) = true;
    else
        Hb_ = Hbar(bad);
        Hu(bad) = C_ap * Hu(bad) + (1 - C_ap) * Hb_;
        Hd(bad) = C_ap * Hd(bad) + (1 - C_ap) * Hb_;
        if strcmp(st.fallback, 'collapse')
            st.Vg(bad) = st.Vg_init(bad);
        end
        st.cav(bad) = false;
    end
end

% Method II
Hu(exists) = Hg2(exists);
Hd(exists) = Hg2(exists);
st.Vg(exists) = Vnew(exists);
st.cav(exists) = true;

% Method I
if any(m1)
    Hg1 = Hbar(m1);
    Veq = st.C3 ./ (Hg1 - hv(m1));                     % Eq. (11)
    if st.limit_growth
        Vo = st.Vg(m1);
        Veq = min(Veq, Vo + max(Vnew(m1) - Vo, 0));
    end
    st.Vg(m1) = Veq;
    Hu(m1) = C_ap * Hu(m1) + (1 - C_ap) * Hg1;         % Eq. (12)
    Hd(m1) = C_ap * Hd(m1) + (1 - C_ap) * Hg1;         % Eq. (13)
    st.cav(m1) = false;
end
H(1:2:end) = Hu; H(2:2:end) = Hd;
end
