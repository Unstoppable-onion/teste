function test_vapour_head()
fl = fluid_properties();
check(abs(fl.Hv - (fl.p_vap - fl.p_bar) / (fl.rho * fl.g)) < 1e-12, 'Hv definition');
check(fl.Hv > -10.2 && fl.Hv < -10.0, 'Hv range');
end
