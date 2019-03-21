function [dayoy]=dm2doy(day,mon,year)
% DM2DOY.M Convert the day month to day-of-year format.
%
% [dayoy]=dm2doy(day,mon,year)
%
% dayoy --- day of year (1-365/366)
% day   --- day (1-31)
% mon   --- month (1-12)
% year  --- year (to sort out leap years)
%
% e.g
% dayoy=dm2doy(17,8,2004)
% [mon,day]=doy2dm(230,2004)
%
% (C) Dr G.J. Frazer August 2004

% check on the inputs
error(nargchk(3,3,nargin));

% decide if leap year or not
if rem(year,4)~=0
  leapFG=0;
elseif rem(year,400)==0
  leapFG=1;
elseif rem(year,100)==0
  leapFG=0;
else
  leapFG=1;
end

% add up days in month
switch mon
  case 1
    dayoy=day;
  case 2
    dayoy=31+day;
  case 3
    dayoy=28+leapFG+31+day;
  case 4
    dayoy=31+28+leapFG+31+day;
  case 5
    dayoy=30+31+28+leapFG+31+day;
  case 6
    dayoy=31+30+31+28+leapFG+31+day;
  case 7
    dayoy=30+31+30+31+28+leapFG+31+day;
  case 8
    dayoy=31+30+31+30+31+28+leapFG+31+day;
  case 9
    dayoy=31+31+30+31+30+31+28+leapFG+31+day;
  case 10
    dayoy=30+31+31+30+31+30+31+28+leapFG+31+day;
  case 11
    dayoy=31+30+31+31+30+31+30+31+28+leapFG+31+day;
  case 12
    dayoy=30+31+30+31+31+30+31+30+31+28+leapFG+31+day;
end