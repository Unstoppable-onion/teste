function s = valid_field(id)
%VALID_FIELD Struct field name from a run id ('fig05_a1e-7' -> 'fig05_a1e_7').
s = regexprep(id, '[^A-Za-z0-9_]', '_');
if isempty(regexp(s(1), '[A-Za-z]', 'once')), s = ['x' s]; end
end
