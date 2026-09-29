function tc = crossings_dig(d, level)
%CROSSINGS_DIG Line-centre crossing times of a digitised curve: runs of
%   consecutive pixel columns whose vertical extent contains the level; the
%   mean abscissa of each run (unbiased with respect to the line width).
span = (d.Hmin <= level) & (d.Hmax >= level);
t = d.t; step = median(diff(t));
tc = [];
i = 1; n = numel(t);
while i <= n
    if span(i)
        j = i;
        while j + 1 <= n && span(j+1) && t(j+1) - t(j) < 1.5 * step
            j = j + 1;
        end
        tc(end+1, 1) = mean(t(i:j)); %#ok<AGROW>
        i = j + 1;
    else
        i = i + 1;
    end
end
end
