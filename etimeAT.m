function [interval]=etimeAT(time2,time1)
% ETIMEAT.M Compute elapsed time from time1 to time2. If time2 is later
% than time1 then interval will be positive. Input variables are in the AT
% (accurate time) structure format.
%
% [interval]=etimeAT(time2,time1)
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
% (C) Dr G J Frazer December 2007

interval=etime([time1.y time1.m time1.d time1.h time1.min time1.s],[time2.y time2.m time2.d time2.h time2.min time2.s]);
return
