function [z,rxinfo,vdflag,rdinfo,onepps]=rddrxspew(fname,todstart,numsecs,msg,tnetuncert)
% RDDRXSPEW.M Read in DDRx SPEW data from a raw file. The start time-of-day
% for the data required and the number of seconds to be extracted can be 
% specified. The extracted data IS TIME SET TO THE 1PPS embedded in the
% data. To facilitate this the data file must be at least 2.1sec long.
%
% VERSION 2.03 17-Dec-2007 (update below in code)
%
% COMMENT:
% The key feature of this script is that it replaces the approximate timing
% of the data file, as specified in the data header and derived from the
% recording computer system time, and hence network time if using NTP, with
% the exact timing as determined from the embedded 1PPS in the data. This
% is absolutely required in order to accurately time align data sets
% recorded on more than one receiver.
%
% [z,rxinfo,vdflag,rdinfo,onepps]=rddrxspew(fname,todstart,numsecs,msg,tnetuncert)
%
% z        --- complex (I/Q) data output from receiver
% rxinfo   --- structure containing receiver parameters
% vdflag   --- valid data flag (0 = okay, -1 = data does not match time 
%               requested)
% rdinfo   --- various information about the read process
% onepps   --- 1PPS signal (same length as z)
% fname    --- file name of SPEW raw data file
% todstart --- time-of-day start time for data extract in the Matlab date 
%               vector format (see note below) [y m d h min s]
% numsecs  --- number of seconds of data file extracted (s) DEFAULT 1
% msg      --- show verbose messages 'n'|'y' DEFAULT 'y'
% tnetuncert - maximum uncertainty time between datafile time and 1PPS 
%               time (seconds) DEFAULT 128e-3
%
% NOTE: 
% The time-of-day start (todstart) is specified in the Matlab date vector
% format (see the help for datevec.m). The rddrxspew script will return a 
% dataset that starts with todstart and lasts numsecs. The todstart IS 
% REFERENCED TO TIMING SET BY THE 1PPS and so can be used for applications 
% requiring accurate time alignment between multiple data files colected 
% using multiple receivers.
%
% It is assumed that the data file time (from the recording computer time)
% is accurate to within the parameter tnetuncert (typ. < 128ms). This value
% should be set to a number larger than the expected uncertainty one gets
% with NTP.
%
% The script is a two pass process. The first pass reads in 2.1s of data so as
% to establish a reliable 1PPS edge. The time offset between computer time
% and 1PPS is established from this 2.1s data. The actual requested 
% data is re-read from the file in a second pass. This supports any TOD so
% long as it is within the file, and supports durations that are less than
% one second.
%
% WARNINGS:
% The function will return an invalid data flag (vdflag) if the requested
% time interval as aligned with 1PPS is not completely available within the
% data file.
%
% Keep in mind that it is possible that data file time (aproximate and 
% derived from computer network time) and 1PPS aligned and corrected 
% time are sufficiently different (up to plus/minus tnetuncert) that a data
% time interval that would seem to be contained in the data file is in fact
% not in the data file. This is notified with a warning message and vdflag.
%
% If the raw data file is less than approximately 2.1 secs in duration then the
% read operation will fail with an error since it will not be possible to
% ensure that the data actually contains at least two 1PPS signals. For this reason,
% always record 2+ secs or more data at a time. This is expected to be the
% case for applications requiring accurate time alignment between data
% recorded on different receivers.
%
% e.g.
% cclo;
% todstart=[2007 12 3 23 54 50.148];
% fname='spew_071203_235440_14000_2500_01_00.S_TEISPII';
% [z,rxinfo,vdflag,rdinfo,onepps]=rddrxspew(fname,todstart);
% spgrm(z, 2.5e6, -1.2e6, 1.2e6, 120, 200, 128, 64);
%
% (C) Dr G.J. Frazer  December 2007 (based on the earlier script
% read_spew_drx.m written by Mr L. Durbridge and Ms L. Lindsay)

% Check inputs
error(nargchk(2,5,nargin));
if nargin<05, tnetuncert=128e-3; end
if nargin<04, msg='y'; end
if nargin<03, numsecs=1; end

%--------------------------------------------------------------------------
% Test input
%cclo;
%todstart=[2007 12 3 23 54 50.148];
%fname='spew_071203_235440_14000_2500_01_00.S_TEISPII';
%fname='spew_071203_235507_14000_2500_01_00.S_TEISPII';
%fname='spew_071204_051631_19000_2500_00_00.S_TEISPII';
%numsecs=1;
%msg='y';
%tnetuncert=50e-3;
% End test input
%--------------------------------------------------------------------------

% Establish output values in case of early termination
z=[]; rxinfo=[]; vdflag=[]; rdinfo=[]; onepps=[];

% version number of this read script
rdinfo.rddrxspew_version=203;

% Parameters
Ver1001=1001;      % Version 1001 of raw data file
vdflag=0;          % valid data set to good data
MinDataLength=2.1; % Min duration of data file in seconds (needed to allow discovery of 1PPS) 

% Get the todstart into AT format
% The AT (accurate time) time structure is defined as:
% 
% time.y   --- year
% time.m   --- month
% time.d   --- day
% time.h   --- hour
% time.min --- minute
% time.s   --- seconds
%
RequestedTODStart.y=todstart(1);
RequestedTODStart.m=todstart(2);
RequestedTODStart.d=todstart(3);
RequestedTODStart.h=todstart(4);
RequestedTODStart.min=todstart(5);
RequestedTODStart.s=todstart(6);

% Print exact TOD start requested
if strcmp(msg,'y')==1
  fprintf(1,'\n    RDDRXSPEW.M messages - START\n\n');
  fprintf(1,'    ... RDDRXSPEW.M Version %4.2f\n',rdinfo.rddrxspew_version/100);
  fprintf(1,'    ... Requested exact TOD start is %s\n',datestrAT(RequestedTODStart,'yyyy-mm-dd HH:MM:SS.FFF'));
  fprintf(1,'    ... Requested data duration is %5.2f s\n',numsecs);
  fprintf(1,'    ... Specified datafile time (NTP) uncertainty (+cle/-) is %5.2f ms\n\n',tnetuncert*1e3);
end

% Read in 2.1 sec of data and dwell flag to get accurate 1PPS timing
[fid, message] = fopen(fname, 'r');
if fid == -1
    error(message);
end

% Read in the file header
rxinfo.version      = fread(fid, 1, 'int32');

%Check the version id and read the data depending on its value
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
rdinfo.DataNTPStartTime=timeATvec(DataNTPStartTime);
if strcmp(msg,'y')==1
  fprintf(1, '    ... RAW datafile header start-time (NTP): %s\n', datestrAT(DataNTPStartTime,'yyyy-mm-dd HH:MM:SS.FFF'));
end

% get remaining data parameters of interest
rxinfo.atten_db        = fread(fid, 1, 'int32');
rxinfo.freq_hz         = fread(fid, 1, 'double');
rxinfo.bw_hz           = fread(fid, 1, 'double');

% We need to determine the actual sample period (in secs) so we can get accurate
% timing
rxinfo.sample_period = round(1e8/rxinfo.bw_hz) * 1e-8;
rxinfo.bw_hz = 1/rxinfo.sample_period;

% Determine the number of samples in the file
stat = dir(fname);
nsamples = (stat.bytes - hdrsize)/8;

% Check that requested data is within data window in file
% Work out time (NTP) extent of data (adjusted for uncertainty)
% Start of data NTP
DataNTPEndTime=addtotimeAT(DataNTPStartTime,(nsamples*rxinfo.sample_period));
rdinfo.DataNTPEndTime=timeATvec(DataNTPEndTime);
if strcmp(msg,'y')==1
  fprintf(1, '    ... RAW datafile sample count end-time (NTP): %s\n', datestrAT(DataNTPEndTime,'yyyy-mm-dd HH:MM:SS.FFF'));
end

% Determine duration of data in RAW file (just as verbose information - not used by code)
DurationDataRAW=etimeAT(DataNTPStartTime,DataNTPEndTime);
rdinfo.DurationDataRAW_secs=DurationDataRAW;
if strcmp(msg,'y')==1
  fprintf(1, '    ... RAW datafile duration is %5.2f s\n\n',DurationDataRAW);
end

% Need at least 2.1s data to determine accurate 1PPS
if DurationDataRAW<MinDataLength
  fprintf(1,'    ... Fatal Warning: Datafile not long enough to discover 1PPS\n');
  fprintf(1,'\n    RDDRXSPEW.M messages - END\n\n');
  vdflag=-1;
  return;
end  

% Read in the first MinDataLength of data to check 1PPS
% Position to start of data to read in
NumSamples=round(MinDataLength/rxinfo.sample_period);

% read the data
[rdat, cnt] = fread(fid, 2*NumSamples, '*uint32');
if cnt ~= 2*NumSamples
    if feof(fid)
        warning('End of file found while reading %s\n', fname);
    else
        error('Short read in file %s\n', fname);
    end
end

% Extract the 1 PPS flag
onepps = bitand(rdat(1:2:end), 2)/2;

% Strip the status bits off the signal and convert to signed doubles
mask = hex2dec('FFFFFFC0');
y = find(bitand(rdat, bitset(0, 32)));  % Find if MSB is set
rdat = double(bitand(rdat, mask));
rdat(y) = -1*(double(intmax('uint32')) - rdat(y))-1;
z = (rdat(1:2:cnt) + j*rdat(2:2:cnt));

% close file since all data now read
fclose(fid);

% Find RISING edges in 1PPS
Rdiff=onepps(2:end)-onepps(1:end-1);
onePPSindexRtemp=find((Rdiff)>0.5);

% Sometime the very first sample is declared to have a transition, ignore
% first reported edge if there are three edges and the first one is at sample 1
if (length(onePPSindexRtemp)==3) && (onePPSindexRtemp(1)==1)
  onePPSindexR=onePPSindexRtemp(2:3);
else
  onePPSindexR=onePPSindexRtemp;
end
onePpsEdgeIndex=onePPSindexR(1);

% Determine number of samples between 1PPS
onePPSSpace=diff(onePPSindexR);
rdinfo.OnePpsSpace_samples=onePPSSpace;
if strcmp(msg,'y')==1
  fprintf(1, '    ... Number of samples between first two 1PPS edges is %7d Ksamples\n',onePPSSpace/1e3);
end

% Determine NTP time of first 1PPS rising edge
TimeNTP1ppsEdge=addtotimeAT(DataNTPStartTime,onePpsEdgeIndex*rxinfo.sample_period);
rdinfo.TimeNTPof1PPSEdge=timeATvec(TimeNTP1ppsEdge);
if strcmp(msg,'y')==1
  fprintf(1, '    ... Data file time (NTP) of 1PPS rising edge (NTP): %s\n', datestrAT(TimeNTP1ppsEdge,'yyyy-mm-dd HH:MM:SS.FFF'));
end

% Find the nearest exact second that must therefore be the true time for
% this 1PPS edge
TrueTime1ppsEdge=TimeNTP1ppsEdge;
TrueTime1ppsEdge.s=round(TimeNTP1ppsEdge.s);
rdinfo.TrueTimeOf1PPSEdge=timeATvec(TrueTime1ppsEdge);
if strcmp(msg,'y')==1
  fprintf(1, '    ... 1PPS rising edge now forced-set to be: %s\n', datestrAT(TrueTime1ppsEdge,'yyyy-mm-dd HH:MM:SS.FFF'));
end

% Report the error between NTP and 1PPS
ppsNtpError=TimeNTP1ppsEdge.s-TrueTime1ppsEdge.s;
rdinfo.OnePPSvNTPerror_secs=ppsNtpError;
if strcmp(msg,'y')==1
  fprintf(1, '    ... NTP v 1PPS error is %5.2f ms\n',ppsNtpError*1e3);
end

if (abs(ppsNtpError))>tnetuncert
  fprintf(1,'    ... Fatal Warning: 1PPS more than NTP uncertainty tolerance from NTP time\n');
  fprintf(1,'\n    RDDRXSPEW.M messages - END\n\n');
  vdflag=-1;
  return;
end

% Determine number of samples error between 1PPS and NTP (positive number
% means get data later in file)
ppsNtpErrorSamples=round(ppsNtpError/rxinfo.sample_period);

% Work out indices of required data in file and correct for error. 
RequiredTODStartTimeFromBof=dtimeAT(DataNTPStartTime,RequestedTODStart);
FirstSample=round(RequiredTODStartTimeFromBof/rxinfo.sample_period)+ppsNtpErrorSamples;
NumSamples=round(numsecs/rxinfo.sample_period);

% Check that still valid read (not asking for data before or after file)
if FirstSample<1
  fprintf(1,'    ... Fatal Warning: Requested data start time is before beginning-of-file so no data extracted\n');
  fprintf(1,'\n    RDDRXSPEW.M messages - END\n\n');
  vdflag=-1;
  return;
end
if FirstSample+NumSamples>nsamples
  fprintf(1,'    ... Fatal Warning: Requested data end time is beyond end-of-file so no data extracted\n');
  fprintf(1,'\n    RDDRXSPEW.M messages - END\n\n');
  vdflag=-1;
  return;
end

% Load in the data
% Open file
[fid, message] = fopen(fname, 'r');
if fid == -1
    error(message);
end
% Read in the data
% Position to start of data to read in
fseek(fid, hdrsize + (FirstSample)*8, 'bof');

% read the data
[rdat, cnt] = fread(fid, 2*NumSamples, '*uint32');
if cnt ~= 2*NumSamples
    if feof(fid)
        warning('End of file found while reading %s\n', fname);
    else
        error('Short read in file %s\n', fname);
    end
end

% Extract the 1 PPS flag
onepps = bitand(rdat(1:2:end), 2)/2;

% Strip the status bits off the signal and convert to signed doubles
mask = hex2dec('FFFFFFC0');
y = find(bitand(rdat, bitset(0, 32)));  % Find if MSB is set
rdat = double(bitand(rdat, mask));
rdat(y) = -1*(double(intmax('uint32')) - rdat(y))-1;
z = (rdat(1:2:cnt) + j*rdat(2:2:cnt));
%z = rdat;
rdinfo.DataReadIn_samples=length(z);

% close file since all required data now read
fclose(fid);
rdinfo.ActuallDataDuration_secs=length(z)*rxinfo.sample_period;
if strcmp(msg,'y')==1
  fprintf(1, '    ... Actual data duration is %5.2f s\n',length(z)*rxinfo.sample_period);
  % Finish all messages
  fprintf(1,'\n    RDDRXSPEW.M messages - END\n\n');
end

%fname_raw=strcat(fname,'.raw')
%
%fid_raw=fopen(fname_raw,'w');
%
%num_sec=length(z)/rxinfo.bw_hz/2;
%
%for i=1:num_sec
%    i_start=(i-1)*rxinfo.bw_hz*2+1;
%    i_end=(i)*rxinfo.bw_hz*2;
%    fwrite(fid_raw,z(i_start:i_end),'int32');    
%    end
%    
%fclose(fid_raw);

