function ft = case_features(name)
%CASE_FEATURES Comparison features per case (same as Python FEATURES):
%   level for event timing (m), plateau windows and peak windows (s).
switch name
    case 'case0'
        ft.level = 23.41; ft.plateaus = {}; ft.peaks = {};
    case 'case1'
        ft.level = 20.0;
        ft.plateaus = {'H_initial', 0.002, 0.018; 'H_joukowsky', 0.03, 0.07; 'H_cavity', 0.09, 0.135};
        ft.peaks = {'peak_2nd_pulse', 0.17, 0.215; 'peak_3rd_pulse', 0.26, 0.33; 'peak_4th_pulse', 0.37, 0.44};
    case 'case2'
        ft.level = 80.0;
        ft.plateaus = {'H_initial', 0.002, 0.018; 'H_joukowsky', 0.03, 0.07; 'H_cavity', 0.10, 0.29};
        ft.peaks = {'peak_2nd_pulse', 0.30, 0.37};
    case 'case3'
        ft.level = 20.0;
        ft.plateaus = {'H_initial', 0.001, 0.0065; 'H_joukowsky', 0.015, 0.06; 'H_cavity', 0.08, 0.12};
        ft.peaks = {'peak_2nd_pulse', 0.16, 0.21; 'peak_3rd_pulse', 0.25, 0.32; ...
                    'peak_4th_pulse', 0.36, 0.44; 'peak_5th_pulse', 0.47, 0.55};
end
end
