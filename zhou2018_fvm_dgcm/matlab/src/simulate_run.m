function [t, H, Hb, meta] = simulate_run(run)
%SIMULATE_RUN Execute one entry of experiments_registry().
%   H = head plotted by the paper "at the valve": last cell I_N (FVM),
%   valve node (MOC) or exact solution (Case 0).  Hb = boundary state
%   U_N+1/2 (FVM only, [] otherwise).
cs = case_parameters(run.case);
switch run.solver
    case 'fvm'
        r = run_fvm(cs, run.num);
        t = r.t; H = r.H_cellN; Hb = r.H_valve; meta = r.meta;
        meta.mass_error_max = max(abs(r.mass_error));
    case 'moc'
        r = run_moc_dgcm(cs, run.num.Ns, run.num.alpha0);
        t = r.t; H = r.H_valve; Hb = []; meta = r.meta;
    case 'exact'
        t = (0:20000)' * (cs.t_end / 20000);
        H = valve_head_exact(cs, t); Hb = []; meta = struct('case', cs.name);
    otherwise
        error('unknown solver %s', run.solver);
end
end
