function [timervec]=timeATvec(timeAT);
% TIMEATVEC.M Convert an AT (accurate time) structure to a time row vector.
%
% [timervec]=timeATvec(timeAT)
%
% timervec  --- [y m d h min s]
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

timervec=[timeAT.y timeAT.m timeAT.d timeAT.h timeAT.min timeAT.s];
return
