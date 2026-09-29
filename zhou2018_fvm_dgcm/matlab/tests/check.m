function check(cond, msg)
%CHECK Assertion helper for the test suite.
if ~cond, error('check failed: %s', msg); end
end
