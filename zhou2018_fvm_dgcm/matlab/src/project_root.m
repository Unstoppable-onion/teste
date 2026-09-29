function r = project_root()
%PROJECT_ROOT Absolute path of the project folder (zhou2018_fvm_dgcm).
here = fileparts(mfilename('fullpath'));       % .../matlab/src
r = fileparts(fileparts(here));
end
