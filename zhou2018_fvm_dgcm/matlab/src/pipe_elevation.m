function z = pipe_elevation(cs, x)
%PIPE_ELEVATION Elevation of the pipe axis (datum = pipe inlet), m.
z = cs.z0 + cs.sin_theta * x;
end
