function [secs]=dtimeAT(time1,time2)
% DTIMEAT.M Determine the time difference between time1 and time2. Time2
% must be later than time1. Time is specified in AT (accurate time) 
% structure format.
%
% [secs]=dtimeAT(time1,time2)
%
% secs  --- time difference from early time (time1) to later time (time2)
%            in seconds. Return of -1 indicates time1 later than time2.
% time1 --- first time (early) (see below)
% time2 --- second time (later)
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
% time1.y=2007; time1.m=12; time1.d=3; time1.h=23; time1.min=54; time1.s=50.148;
% time2.y=2007; time2.m=12; time2.d=4; time2.h=23; time2.min=55; time2.s=50.148000001;
% secs=dtimeAT(time1,time2);
% fprintf(1,'   %13.9f\n',secs);
% 
% (C) Dr G J Frazer December 2007

% Check inputs
error(nargchk(2,2,nargin));

%--------------------------------------------------------------------------
% Test input
% cclo;
% time1.y=2007; time1.m=12; time1.d=3; time1.h=23; time1.min=54; time1.s=50.148;
% time2.y=2007; time2.m=12; time2.d=3; time2.h=23; time2.min=55; time2.s=50.148000001;
% cclo;
% time1.y=2007; time1.m=12; time1.d=9; time1.h=10; time1.min=0; time1.s=59.728;
% time2.y=2007; time2.m=12; time2.d=9; time2.h=10; time2.min=1; time2.s=7;
% End test input
%--------------------------------------------------------------------------

% Do in two parts (whole seconds and fractional seconds)
% Fractional seconds
secdiff=(time2.s-floor(time2.s))-(time1.s-floor(time1.s));

% Get difference of whole seconds part
time1A=time1;
time1A.s=floor(time1A.s);
time2A=time2;
time2A.s=floor(time2A.s);

% convert to datenum but okay since we are working only with whle seconds
time1ADN=datenum([time1A.y time1A.m time1A.d time1A.h time1A.min time1A.s]);
time2ADN=datenum([time2A.y time2A.m time2A.d time2A.h time2A.min time2A.s]);

% convert the difference into whole seconds
totalsecdiff=round((24*3600)*(time2ADN-time1ADN));

% Adjust by fractional seconds
secs=totalsecdiff+secdiff;

% Confirm that time1 is earlier than time2
if secs<0, secs=-1; end
return;




