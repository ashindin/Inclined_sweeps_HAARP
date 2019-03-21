function [tsof,version]=gettsofspew(fname,msg)
% GETTSOFSPEW.M Get the time-of-data in the RAW SPEW data file. The value
% is returned as a Matlab date number.
%
% % VERSION 1.02 17-Dec-2007
%
% [tsof]=gettsofspew(fname)
%
% tsof     --- time-of-day start of RAW file in accurate time AT format
% fname    --- file name of SPEW raw data file
% msg      --- show verbose messages 'n'|'y' DEFAULT 'y'
%
% The AT (accurate time) time structure is defined as:
% 
% time.y   --- year
% time.m   --- month
% time.d   --- day
% time.h   --- hour
% time.min --- minute
% time.s   --- seconds
%
% e.g.
% cclo;
% fname='spew_071203_235440_14000_2500_01_00.S_TEISPII';
% tsof=gettsofspew(fname);
% % Add one second to tsof
% tsof.s=tsof.s+1;
% datestrAT(tsof,'yyyy-mm-dd HH:MM:SS.FFF')
%
% (C) Dr G.J. Frazer  December 2007 

% Check inputs
error(nargchk(1,2,nargin));
if nargin<02, msg='n'; end

% Version of script
version=102;

%--------------------------------------------------------------------------
% Test input
% cclo;
% msg='y';
% fname='spew_071203_235440_14000_2500_01_00.S_TEISPII';
% End test input
%--------------------------------------------------------------------------

% Parameters
Ver1001=1001; % Version 1001 of raw data file

% Open file
[fid, message] = fopen(fname, 'r');
if fid == -1
    error(message);
end

% Read in the file header
rxinfo.version      = fread(fid, 1, 'int32');

% Check the version id and read the data depending on its value
if (rxinfo.version == Ver1001)
  hdrsize = 36;
else
  % Assume the file is the original format.
  hdrsize = 32;
end

% get the data time from the file - accurate only to network time standard
start_time_sec         = fread(fid, 1, 'uint32');
start_time_usec        = fread(fid, 1, 'uint32');
start_time_days        = (start_time_sec + start_time_usec/1000000) / (24*3600);
jan01_1970             = datenum('01-jan-1970');

rxinfo.start_time      = jan01_1970 + start_time_days;
rxinfo.start_time_sec  = start_time_sec;
rxinfo.start_time_usec = start_time_usec;

start_time_base = jan01_1970 + (start_time_sec) / (24*3600);
StartDataNTP=start_time_base + (start_time_usec/1000000)/(24*3600);

% Data file time (as determined by NTP) stored in accurate time format
DataNTPStartTime=datevecAT(StartDataNTP);
tsof=DataNTPStartTime;

% Print the RAW file time 
if strcmp(msg,'y')==1
  fprintf(1, '    ... RAW datafile header start-time (NTP): %s\n', datestrAT(DataNTPStartTime,'yyyy-mm-dd HH:MM:SS.FFF'));
end

% close the file
fclose(fid);



