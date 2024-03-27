function PCO20S2 = import_sim_timeseries2(workbookFile, sheetName, dataLines)
%IMPORTFILE Import data from a spreadsheet
%  PCO20S2 = IMPORTFILE(FILE) reads data from the first worksheet in the
%  Microsoft Excel spreadsheet file named FILE.  Returns the data as a
%  table.
%
%  PCO20S2 = IMPORTFILE(FILE, SHEET) reads from the specified worksheet.
%
%  PCO20S2 = IMPORTFILE(FILE, SHEET, DATALINES) reads from the specified
%  worksheet for the specified row interval(s). Specify DATALINES as a
%  positive scalar integer or a N-by-2 array of positive scalar integers
%  for dis-contiguous row intervals.
%
%  Example:
%  PCO20S2 = importfile("C:\Users\cemke\MasterProject\05_Results\degradation_pareto_finished_yearly_4\[PCO2_0.01]_v1_annual__01_02_21_47_13.xlsx", "schedule", [2, Inf]);
%
%  See also READTABLE.
%
% Auto-generated by MATLAB on 15-Sep-2023 10:30:22

%% Input handling

% If no sheet is specified, read first sheet
if nargin == 1 || isempty(sheetName)
    sheetName = 1;
end

% If row start and end points are not specified, define defaults
if nargin <= 2
    dataLines = [2, Inf];
end

%% Set up the Import Options and import the data
opts = spreadsheetImportOptions("NumVariables", 11);

% Specify sheet and range
opts.Sheet = sheetName;
opts.DataRange = dataLines(1, :);

% Specify column names and types
opts.VariableNames = ["VarName1",'pcc_feedin_schedule', 'pcc_schedule', "ts", 'cumulative_grid_cost' , "pcc_purchase_schedule", "cumulative_degr_cost", "soc_schedule", "DP", 'grid_electricity_price', "money_balance_grid", 'co2_balance_grid', 'degradation'];
opts.VariableTypes = ["double", 'double', 'double', "datetime", 'double','double','double','double','double','double','double','double','double'];

% Import the data
PCO20S2 = readtable(workbookFile, opts, "UseExcel", false);

for idx = 2:size(dataLines, 1)
    opts.DataRange = dataLines(idx, :);
    tb = readtable(workbookFile, opts, "UseExcel", false);
    PCO20S2 = [PCO20S2; tb]; %#ok<AGROW>
end

end