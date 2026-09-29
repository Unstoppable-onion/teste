function runs = experiments_registry()
%EXPERIMENTS_REGISTRY All simulations needed to reproduce Figs. 4-11
%   (same definitions as python/fvmdgcm/experiments.py).
%   Each run: id, fig, case, solver ('fvm' | 'moc' | 'exact'), dig
%   (digitised paper series in data/digitized) and num (numerical options).
runs = {};
panels = 'abcd';
caps4 = [1.0 0.9 0.5 0.0];
for k = 1:4
    p = panels(k);
    for order = 1:2
        runs{end+1} = mk(sprintf('fig04%s_o%d', p, order), 'fig04', 'case0', 'fvm', ...
            sprintf('fig04_%s_numerical', p), numerics_default('Ns', 32, 'Cr', 1.0, ...
            'C_ap', caps4(k), 'order', order, 'alpha0', 1e-7)); %#ok<*AGROW>
    end
    runs{end+1} = mk(sprintf('fig04%s_exact', p), 'fig04', 'case0', 'exact', ...
        sprintf('fig04_%s_exact', p), struct());
end
a0 = [1e-7 1e-8 1e-10]; tags = {'a1e-7', 'a1e-8', 'a1e-10'};
for k = 1:3
    runs{end+1} = mk(['fig05_' tags{k}], 'fig05', 'case1', 'fvm', ['fig05_main_' tags{k}], ...
        numerics_default('Ns', 32, 'Cr', 1.0, 'C_ap', 0.9, 'order', 2, 'alpha0', a0(k)));
end
caps6 = [1.0 0.9 0.8 0.5];
for k = 1:4
    for Ns = [32 256]
        runs{end+1} = mk(sprintf('fig06%s_Ns%d', panels(k), Ns), 'fig06', 'case1', 'fvm', ...
            sprintf('fig06_%s_Ns%d', panels(k), Ns), numerics_default('Ns', Ns, 'Cr', 1.0, ...
            'C_ap', caps6(k), 'order', 2, 'alpha0', 1e-7));
    end
end
for C = [1.0 0.9]
    runs{end+1} = mk(sprintf('fig07_Cap%.1f', C), 'fig07', 'case2', 'fvm', ...
        sprintf('fig07_main_Cap%.1f', C), numerics_default('Ns', 32, 'Cr', 1.0, 'C_ap', C, ...
        'order', 2, 'alpha0', 1e-7));
end
for C = [1.0 0.9]
    runs{end+1} = mk(sprintf('fig08_Cap%.1f', C), 'fig08', 'case3', 'fvm', ...
        sprintf('fig08_main_Cap%.1f', C), numerics_default('Ns', 256, 'Cr', 1.0, 'C_ap', C, ...
        'order', 2, 'alpha0', 1e-7));
end
pp = 'ab';
for order = 1:2
    for Cr = [1.0 0.5 0.1]
        runs{end+1} = mk(sprintf('fig09%s_Cr%.1f', pp(order), Cr), 'fig09', 'case1', 'fvm', ...
            sprintf('fig09_%s_Cr%.1f', pp(order), Cr), numerics_default('Ns', 32, 'Cr', Cr, ...
            'C_ap', 0.9, 'order', order, 'alpha0', 1e-7));
    end
end
for Ns = [32 256]
    runs{end+1} = mk(sprintf('fig10_Ns%d', Ns), 'fig10', 'case1', 'fvm', ...
        sprintf('fig10_main_Ns%d', Ns), numerics_default('Ns', Ns, 'Cr', 1.0, 'C_ap', 1.0, ...
        'order', 2, 'model', 'DVCM', 'alpha0', 0.0));
end
for Ns = [32 256]
    runs{end+1} = mk(sprintf('fig11_Ns%d', Ns), 'fig11', 'case1', 'moc', ...
        sprintf('fig11_main_Ns%d', Ns), struct('Ns', Ns, 'alpha0', 1e-7));
end
end

function r = mk(id, fig, cs, solver, dig, num)
r = struct('id', id, 'fig', fig, 'case', cs, 'solver', solver, 'dig', dig);
r.num = num;
end
