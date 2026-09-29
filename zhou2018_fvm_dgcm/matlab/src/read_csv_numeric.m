function M = read_csv_numeric(file)
%READ_CSV_NUMERIC Numeric content of a CSV file with one header line.
M = dlmread(file, ',', 1, 0);
end
