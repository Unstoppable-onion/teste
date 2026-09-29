function make_figures()
%MAKE_FIGURES Reproduce Figs. 4-11 of Zhou et al. (2018) from the MATLAB
%   results (results/matlab) and overlay the digitised paper curves (grey
%   dots) and the digitised experiment (thick black).
%   Output: results/figures_matlab/figNN.png
setup_paths();
if exist('OCTAVE_VERSION', 'builtin') > 0 && isempty(getenv('DISPLAY'))  % needs a display (e.g. xvfb-run)
    graphics_toolkit('gnuplot');   % headless Octave (no effect in MATLAB)
end
root = project_root();
out = fullfile(root, 'results', 'figures_matlab');
if ~exist(out, 'dir'), mkdir(out); end
red = [0.84 0.15 0.16]; blue = [0.12 0.25 0.75]; grey = [0.55 0.55 0.55]; blk = [0 0 0];
Y1 = [-20 20 60 100 140];

% ---- Fig. 4 (Case 0)
f = figure('visible', 'off', 'position', [0 0 1200 700]);
caps = [1.0 0.9 0.5 0.0]; pn = 'abcd';
for k = 1:4
    subplot(2, 2, k);
    series = {sprintf('fig04%s_exact', pn(k)), 'Exact', grey, 2.5; ...
              sprintf('fig04%s_o2', pn(k)), '2nd FVM-DGCM', red, 1.2; ...
              sprintf('fig04%s_o1', pn(k)), '1st FVM-DGCM', blue, 0.8};
    panel(series, '', [0 1], [0 60], [0 20 40 60], ...
          sprintf('(%s) Case 0, C_{-ap} = %.1f', pn(k), caps(k)));
end
save_fig(f, fullfile(out, 'fig04.png'));

% ---- Fig. 5
f = figure('visible', 'off', 'position', [0 0 800 450]);
panel({'fig05_a1e-10', '\alpha_0 = 1e-10', grey, 1.2; 'fig05_a1e-8', '\alpha_0 = 1e-8', red, 1.2; ...
       'fig05_a1e-7', '\alpha_0 = 1e-7', blue, 1.2}, 'fig05_main_experiment', [0 0.45], ...
      [-20 160], Y1, 'Fig. 5 - Case 1, 2nd FVM-DGCM');
save_fig(f, fullfile(out, 'fig05.png'));

% ---- Fig. 6
f = figure('visible', 'off', 'position', [0 0 1200 700]);
caps = [1.0 0.9 0.8 0.5];
for k = 1:4
    subplot(2, 2, k);
    panel({sprintf('fig06%s_Ns256', pn(k)), 'Ns = 256', grey, 1.0; ...
           sprintf('fig06%s_Ns32', pn(k)), 'Ns = 32', red, 1.2}, ...
          sprintf('fig06_%s_experiment', pn(k)), [0 0.45], [-20 160], Y1, ...
          sprintf('(%s) Case 1, C_{-ap} = %.1f', pn(k), caps(k)));
end
save_fig(f, fullfile(out, 'fig06.png'));

% ---- Fig. 7, 8
f = figure('visible', 'off', 'position', [0 0 800 450]);
panel({'fig07_Cap1.0', 'C_{-ap} = 1.0', grey, 1.8; 'fig07_Cap0.9', 'C_{-ap} = 0.9', red, 1.2}, ...
      'fig07_main_experiment', [0 0.45], [-20 230], [-20 30 80 130 180 230], 'Fig. 7 - Case 2 (Ns = 32)');
save_fig(f, fullfile(out, 'fig07.png'));
f = figure('visible', 'off', 'position', [0 0 800 450]);
panel({'fig08_Cap1.0', 'C_{-ap} = 1.0', grey, 1.8; 'fig08_Cap0.9', 'C_{-ap} = 0.9', red, 1.2}, ...
      'fig08_main_experiment', [0 0.57], [-20 140], [-20 10 40 70 100 130], 'Fig. 8 - Case 3 (Ns = 256)');
save_fig(f, fullfile(out, 'fig08.png'));

% ---- Fig. 9
f = figure('visible', 'off', 'position', [0 0 800 800]);
ords = {'1st', '2nd'}; pp = 'ab';
for k = 1:2
    subplot(2, 1, k);
    panel({sprintf('fig09%s_Cr1.0', pp(k)), 'Cr = 1.0', blk, 1.2; ...
           sprintf('fig09%s_Cr0.5', pp(k)), 'Cr = 0.5', red, 1.2; ...
           sprintf('fig09%s_Cr0.1', pp(k)), 'Cr = 0.1', blue, 1.2}, '', [0 0.45], [-20 160], Y1, ...
          sprintf('(%s) Case 1, C_{-ap} = 0.9, %s order', pp(k), ords{k}));
end
save_fig(f, fullfile(out, 'fig09.png'));

% ---- Fig. 10, 11
lab = {'2nd FVM-DVCM', 'MOC-DGCM'}; fid = {'fig10', 'fig11'};
for k = 1:2
    f = figure('visible', 'off', 'position', [0 0 800 450]);
    panel({[fid{k} '_Ns256'], [lab{k} ' (Ns = 256)'], grey, 1.0; ...
           [fid{k} '_Ns32'], [lab{k} ' (Ns = 32)'], red, 1.2}, [fid{k} '_main_experiment'], ...
          [0 0.45], [-20 160], Y1, sprintf('Fig. %s - Case 1', fid{k}(4:5)));
    save_fig(f, fullfile(out, [fid{k} '.png']));
end
fprintf('figures written to %s\n', out);
end

function panel(series, exp_key, xl, yl, yt, ttl)
root = project_root();
runs = experiments_registry();
hold on;
h = []; names = {};
if ~isempty(exp_key)
    d = load_digitized(exp_key);
    h(end+1) = plot(d.t, d.H, '-', 'color', [0 0 0], 'linewidth', 2.2);
    names{end+1} = 'Experiment (digitised)';
end
for k = 1:size(series, 1)
    M = read_csv_numeric(fullfile(root, 'results', 'matlab', [series{k, 1} '.csv']));
    h(end+1) = plot(M(:, 1), M(:, 2), '-', 'color', series{k, 3}, 'linewidth', series{k, 4}); %#ok<AGROW>
    names{end+1} = series{k, 2}; %#ok<AGROW>
end
for k = 1:size(series, 1)
    for r = 1:numel(runs)
        if strcmp(runs{r}.id, series{k, 1})
            d = load_digitized(runs{r}.dig);
            hp = plot(d.t, d.H, '.', 'color', [0.45 0.45 0.45], 'markersize', 3);
            if k == 1, h(end+1) = hp; names{end+1} = 'paper (digitised)'; end %#ok<AGROW>
        end
    end
end
hold off;
xlim(xl); ylim(yl); set(gca, 'ytick', yt);
xlabel('t (s)'); ylabel('H (m)'); title(ttl);
legend(h, names, 'location', 'northeast');
box on;
end

function save_fig(f, file)
print(f, file, '-dpng', '-r110');
close(f);
end
