function [mon,day]=doy2dm(dayoy,year)
% DOY2DM.M Convert the day-of-year to day month format.
%
% [mon,day]=doy2dm(dayoy,year)
%
% mon   --- month (1-12)
% day   --- day (1-31)
% dayoy --- day of year (1-365/366)
% year  --- year (to sort out leap years)
%
% e.g
% [mon,day]=doy2dm(230,2004)
% dayoy=dm2doy(17,8,2004)
%
% (C) Dr G.J. Frazer August 2004

% check on the inputs
error(nargchk(2,2,nargin));

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

% Convert to month day
jan=31;
feb=28;
mar=31;
apr=30;
may=31;
jun=30;
jul=31;
aug=31;
sep=30;
oct=31;
nov=30;
dec=31;
if leapFG==1, feb=29; end

if dayoy>=1 & dayoy<=jan
  mon=1;
  day=dayoy;
elseif dayoy>=(jan+1) & dayoy<=(jan+feb)
  mon=2;
  day=dayoy-jan;
elseif dayoy>=(jan+feb+1) & dayoy<=(jan+feb+mar)
  mon=3;
  day=dayoy-(jan+feb);
elseif dayoy>=(jan+feb+mar+1) & dayoy<=(jan+feb+mar+apr)
  mon=4;
  day=dayoy-(jan+feb+mar);
elseif dayoy>=(jan+feb+mar+apr+1) & dayoy<=(jan+feb+mar+apr+may)
  mon=5;
  day=dayoy-(jan+feb+mar+apr);
elseif dayoy>=(jan+feb+mar+apr+may+1) & dayoy<=(jan+feb+mar+apr+apr+may+jun)
  mon=6;
  day=dayoy-(jan+feb+mar+apr+may);
elseif dayoy>=(jan+feb+mar+apr+may+jun+1) & dayoy<=(jan+feb+mar+apr+may+jun+jul)
  mon=7;
  day=dayoy-(jan+feb+mar+apr+may+jun);
elseif dayoy>=(jan+feb+mar+apr+may+jun+jul+1) & dayoy<=(jan+feb+mar+apr+may+jun+jul+aug)
  mon=8;
  day=dayoy-(jan+feb+mar+apr+may+jun+jul);
elseif dayoy>=(jan+feb+mar+apr+may+jun+jul+aug+1) & dayoy<=(jan+feb+mar+apr+may+jun+jul+aug+sep)
  mon=9;
  day=dayoy-(jan+feb+mar+apr+may+jun+jul+aug);
elseif dayoy>=(jan+feb+mar+apr+may+jun+jul+aug+sep+1) & dayoy<=(jan+feb+mar+apr+may+jun+jul+aug+sep+oct)
  mon=10;
  day=dayoy-(jan+feb+mar+apr+may+jun+jul+aug+sep);
elseif dayoy>=(jan+feb+mar+apr+may+jun+jul+aug+sep+oct+1) & dayoy<=(jan+feb+mar+apr+may+jun+jul+aug+sep+oct+nov)
  mon=11;
  day=dayoy-(jan+feb+mar+apr+may+jun+jul+aug+sep+oct);
elseif dayoy>=(jan+feb+mar+apr+may+jun+jul+aug+sep+oct+nov+1) & dayoy<=(jan+feb+mar+apr+may+jun+jul+aug+sep+oct+nov+dec)
  mon=12;
  day=dayoy-(jan+feb+mar+apr+may+jun+jul+aug+sep+oct+nov);
else
  mon=[];
  day=[];
  error('   ... invalid day of year');
end
return;
  



