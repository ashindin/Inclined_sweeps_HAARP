function [newtime]=addtotimeAT(time,secs)
% ADDTOTIMEAT.M Add a specified number of seconds to a time specified in
% AT (accurate time) structure format. The time increment secs must be
% positive (cannot substract time). 
%
% [newtime]=addtotimeAT(time,secs)
%
% newtime - new time is time plus secs
% time  --- time (see below)
% secs  --- seconds to add to time (>0) or else newtime=-1;
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
% clear all; close all;
% timenum=datenum('03-Dec-2007 23:54:50.148');
% time=datevecAT(timenum);
% secs=15+300+28*24*3600;
% time
% newtime=addtotimeAT(time,secs)
% 
% (C) Dr G J Frazer December 2007

% Check inputs
error(nargchk(2,2,nargin));

% Check that input time increment is positive
if secs<0
  newtime=-1;
  return;
end

% Allocate output structure
newtime.y=[];
newtime.m=[];
newtime.d=[];
newtime.h=[];
newtime.min=[];
newtime.s=[];

% Add secs to time
newsecs=time.s+secs;                  % total number of seconds (but many of these may be minutes, hours, etc)
residualsecs=rem(newsecs,60);         % find just the residual seconds
newtime.s=residualsecs;               % set the output time seconds to the residual number of seconds and carry the minutes

% Add carry minutes and work out minutes total and residual
carrymins=fix(newsecs/60);            
newmins=time.min+carrymins;
residualmins=rem(newmins,60);       
newtime.min=residualmins;  

% Add carry hours and work out hours total and residual
carryhours=fix(newmins/60);
newhours=time.h+carryhours;
residualhours=rem(newhours,24);
newtime.h=residualhours;

% Add carry days
carrydays=fix(newhours/24);

% Convert year month day to day of year
dayoy=dm2doy(time.d,time.m,time.y);

% Add the carry days
newdoy=dayoy+carrydays;

% Decide if leap year or not
if rem(time.y,4)~=0
  leapFG=0;
elseif rem(time.y,400)==0
  leapFG=1;
elseif rem(time.y,100)==0
  leapFG=0;
else
  leapFG=1;
end

% Add carry days and work out years total and days residual
% No zero day of year (1-365/366)
if leapFG==1
  carryyears=fix((newdoy-1)/366);
else
  carryyears=fix((newdoy-1)/365);
end
newtime.y=time.y+carryyears;
if leapFG==1
  residualyears=rem(newdoy-1,365)+1;
else
  residualyears=rem(newdoy-1,365)+1;
end
newdoy=residualyears;

% update both month and day
[newtime.m,newtime.d]=doy2dm(newdoy,newtime.y);
return
