function [time]=datevecAT(timenum);
% DATEVECAT.M Convert a Matlab date number to an AT (accurate time) 
% structure format.
%
% [time]=datevecAT(timenum)
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

[time.y time.m time.d time.h time.min time.s]=datevec(timenum);
return
