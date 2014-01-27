function [accel] = accel_input(Amax,Vmax,Distance,StartTime,CurrTime,Shaper)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% function [accel] = accel_input(Amax,Vmax,Distance,CurrTime,Shaper)
%
% Function returns acceleration at a given timestep based on user input
%
% Amax = maximum accel, assumed to besymmetric +/-
% Vmax = maximum velocity, assumed to be symmetric in +/-
% Distance = desired travel distance 
% StartTime = Time command should begin
% CurrTime = current time 
% Shaper = array of the form [Ti Ai] - matches output format of shaper functions
%           in toolbox
%          * If no Shaper input is given, then unshaped in run
%          * If Shaper is empty, then unshaped is run
%
%
% Assumptions:
%   * +/- maximums are of same amplitude
%   * command will begin at StartTime (default = 0)
%   * rest-to-rest bang-coast-bang move (before shaping)
%
% Created: 9/23/11 - Joshua Vaughan - vaughanje@gatech.edu
%
% Modified: 
%   10/11/11 - Added hard-coded shaping option - JEV (vaughanje@gatech.edu)
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% These are the times for a bang-bang input 
t1 = StartTime;
t2 = (Vmax/Amax) + t1;
t3 = (Distance/Vmax) + t1;
t4 = (t2 + t3)-t1;

if nargin == 5 || isempty(Shaper)
	% If no shaper is input, create an unshaped command
    if t3 <= t2 % command should be bang-bang, not bang-coast-bang
    	t2 = sqrt(Distance/Amax)+t1;
    	t3 = 2*sqrt(Distance/Amax)+t1;
    	
    	accel = Amax*heaviside(CurrTime-t1) - 2*Amax*heaviside(CurrTime-t2) + Amax*heaviside(CurrTime-t3);
    
    else % command is bang-coast-bang
		accel = Amax*heaviside(CurrTime-t1) - Amax*heaviside(CurrTime-t2) - Amax*heaviside(CurrTime-t3) + Amax*heaviside(CurrTime-t4);
	end
	
else % create a shaped command
    % Parse Shaper parameters
    for ii = 1:length(Shaper)
        ts(ii) = Shaper(ii,1);  % Shaper impulse times
        A(ii) = Shaper(ii,2);   % Shaper impulse amplitudes
    end
    
    % Fill remaining impulses and times with zeros
    for ii = length(Shaper)+1:9
        ts(ii) = 0;
        A(ii) = 0;
    end
    
    if length(Shaper) > 9
        error('Error: As of 10/11/11, accel_input.m only works for shapers of less than 9 impulses.');
    end

    % Attempts at a more elegant solution... no time, just hard-coded for now, 10/11/11 
    %     for ii = 1:length(Shaper)
    %         accel = accel + A(ii)*(Amax*heaviside(CurrTime-(t1+ts(ii))) - Amax*heaviside(CurrTime-(t2+ts(ii))) - Amax*heaviside(CurrTime-(t3+ts(ii))) + Amax*heaviside(CurrTime-(t4-ts(ii))))
    %     end
    %     accel = sum(A.*(Amax*heaviside(CurrTime-(t1+ts)) - Amax*heaviside(CurrTime-(t2+ts)) - Amax*heaviside(CurrTime-(t3+ts)) + Amax*heaviside(CurrTime-(t4-ts))));


    % Hard-coded for now
    % TODO: be smarter about constructing the total input - JEV - 10/11/11
    accel = A(1)*(Amax*heaviside(CurrTime-(t1+ts(1))) - Amax*heaviside(CurrTime-(t2+ts(1))) - Amax*heaviside(CurrTime-(t3+ts(1))) + Amax*heaviside(CurrTime-(t4-ts(1))))...
        +   A(2)*(Amax*heaviside(CurrTime-(t1+ts(2))) - Amax*heaviside(CurrTime-(t2+ts(2))) - Amax*heaviside(CurrTime-(t3+ts(2))) + Amax*heaviside(CurrTime-(t4+ts(2))))...
        +   A(3)*(Amax*heaviside(CurrTime-(t1+ts(3))) - Amax*heaviside(CurrTime-(t2+ts(3))) - Amax*heaviside(CurrTime-(t3+ts(3))) + Amax*heaviside(CurrTime-(t4+ts(3))))...
        +   A(4)*(Amax*heaviside(CurrTime-(t1+ts(4))) - Amax*heaviside(CurrTime-(t2+ts(4))) - Amax*heaviside(CurrTime-(t3+ts(4))) + Amax*heaviside(CurrTime-(t4+ts(4))))...
        +   A(5)*(Amax*heaviside(CurrTime-(t1+ts(5))) - Amax*heaviside(CurrTime-(t2+ts(5))) - Amax*heaviside(CurrTime-(t3+ts(5))) + Amax*heaviside(CurrTime-(t4+ts(5))))...
        +   A(6)*(Amax*heaviside(CurrTime-(t1+ts(6))) - Amax*heaviside(CurrTime-(t2+ts(6))) - Amax*heaviside(CurrTime-(t3+ts(6))) + Amax*heaviside(CurrTime-(t4+ts(6))))...
        +   A(7)*(Amax*heaviside(CurrTime-(t1+ts(7))) - Amax*heaviside(CurrTime-(t2+ts(7))) - Amax*heaviside(CurrTime-(t3+ts(7))) + Amax*heaviside(CurrTime-(t4+ts(7))))...
        +   A(8)*(Amax*heaviside(CurrTime-(t1+ts(8))) - Amax*heaviside(CurrTime-(t2+ts(8))) - Amax*heaviside(CurrTime-(t3+ts(8))) + Amax*heaviside(CurrTime-(t4+ts(8))))...
        +   A(9)*(Amax*heaviside(CurrTime-(t1+ts(9))) - Amax*heaviside(CurrTime-(t2+ts(9))) - Amax*heaviside(CurrTime-(t3+ts(9))) + Amax*heaviside(CurrTime-(t4+ts(9))));
end