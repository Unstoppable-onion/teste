function setup_paths()
%SETUP_PATHS Add the source and test folders of the MATLAB port to the path.
here = fileparts(mfilename('fullpath'));
addpath(fullfile(here, 'src'));
addpath(fullfile(here, 'tests'));
end
