% for "driving"
Amax = 1;                  % maximum accleration of trolley (m/s^2)
Vmax = 0.35;               % maximum velocity of trolleys (m/s)
Distance= 0.5;               % Desired move distnace
StartTime = 0.5;           % Time the command should start
Shaper = [];

t = 0:0.01:10;

accel = accel_input(Amax,Vmax,Distance,StartTime,t,Shaper)

plot(t,accel)