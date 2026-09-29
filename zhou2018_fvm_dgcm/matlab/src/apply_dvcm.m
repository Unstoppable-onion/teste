function [st, H] = apply_dvcm(st, H, Q, dt)
%APPLY_DVCM Discrete vapour cavity correction (FVM-DVCM, Zhou et al. 2017):
%   a cavity forms when a half is at/below the vapour head, its volume
%   follows continuity (Eq. 15), its head is the vapour head, and it
%   collapses (volume 0, FVM heads kept) when the volume becomes <= 0.
Hu = H(1:2:end); Hd = H(2:2:end);
Qu = Q(1:2:end); Qd = Q(2:2:end);
hv = st.hvap;
use = st.cav | (min(Hu, Hd) <= hv);
Vnew = st.Vg + (Qd - Qu) * dt;
exists = use & (Vnew > 0);
Hu(exists) = hv(exists);
Hd(exists) = hv(exists);
st.Vg = zeros(size(Vnew));
st.Vg(exists) = Vnew(exists);
st.cav = exists;
H(1:2:end) = Hu; H(2:2:end) = Hd;
end
