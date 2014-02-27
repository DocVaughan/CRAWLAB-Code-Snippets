%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% A template to help create readable figures 
%   (a contrast the default MATLAB/Octave output)
%
% It may actually look worse on screen. The saved version should be better.
%
% This will just plot junk data. Copy and paste into your script, then...
%
% You will have to fill in:
%   - the actual things to plot
%   - the axis labels - be sure to include units - lines 103-104
%   - the legend labels - line 107
%   - the filename to save the figure as - line 118 or 121
%
% You will likely have to change:
%   - axes limits - Line 100
%   - the page margins, based on data and labeling - Line 75
%   - the legend location and/or number of columns - Lines 103-104
%
% Created: 4/19/13 - Joshua Vaughan (joshua.vaughan@louisiana.edu)
%
% Modified: 
%   * 6/14/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu
%       - now changes options based on MATLAB or Octave
%   * 2/26/14 - Joshua Vaughan - joshua.vaughan@louisiana.edu
%       - removed top and right axes borders
%       - adjusted page margins to better fill the page. NOTE: These often 
%         need to be adjusted based on the data
%       - more explicit suggestion of what needs to be changed
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Example data so that code will show a plot... 
x1 = 0:0.01:6;
x2 = x1;
x3 = x1;
x4 = x1;

y1 = sin(x1);
y2 = 0.5*sin(x2);
y3 = 0.75*sin(x3);
y4 = 1.25*sin(x4);



%-----  Copy from here down into your code, replacing items as needed ----------------
%
% Decide if user is using MATLAB or Octave
% This will return a nonzero value if in Octave
isOctave = exist('OCTAVE_VERSION');

if isOctave == 0 % We're in MATLAB
    plot_line_width = 3;
    grid_line_width = 2;
else % We're in Octave
    plot_line_width = 8;
    grid_line_width = 2;
end

% Set consistent font
font_name = 'Times New Roman';

%  The plot is formatted for saving, so it might be ugly on screen
h = figure;

% Define the papersize and margins
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');

% papersize is 9" x 6" - 3x2 aspect ratio is best
set (h,'papersize',[9 6])       
set (h,'paperposition', [0,0,[9 6]])

% set the margins as percentage of page 
%---- You may need to change this based on the scale of your data --------%
% format is:
%    [left marging, bottom margin, horiz size, vert size] as % of page size
if isOctave == 0; % this is MATLAB
    set (gca,'position', [0.12, 0.12, 0.85, 0.85]);
else
    set (gca, 'position', [0.13, 0.11, 0.80, 0.85]);
end

set(gca, 'ActivePositionProperty', 'OuterPosition')

% The options are only specified once in MATLAB. Octave let's you adjust
% each line. This means we need to define the LineWidth for each variable
% in Octave.
if isOctave == 0 % We're in MATLAB
    % This is the actual plotting... Change xi and yi
    plot(x1,y1,x2,y2,'--',x3,y3,'-.',x4,y4,'k:','LineWidth',plot_line_width)
else % We're in Octave 
    % This is the actual plotting... Change xi and yi
    plot(x1,y1,'LineWidth',plot_line_width,x2,y2,'--','LineWidth',plot_line_width,x3,y3,'-.','LineWidth',plot_line_width,x4,y4,'k:','LineWidth',plot_line_width)
end

% Show a grid and set an appropriate line thickness 
grid on
set (gca, 'LineWidth',grid_line_width)

% Remove the top and right axes lines
set (gca, 'box', 'off')

% Increase the axis font size to something readable
set (gca, 'fontsize', 24)

%---- You will need to change this based on the scale of your data -------%
% Set the axis limits - [xmin xmax ymin max]
axis([0 5 -2 2])

% Set the X and Y axis labels - Change these to suit your plot
xlabel('X Label (units)','fontsize',28)
ylabel('Y Label (units)','fontsize',28)

% Create the legend - change 'Data i' to suit your plot
leg = legend('Data 1 ','Data 2 ','Data 3 ','Data 4 ');
set (leg, 'FontSize', 22,'FontName',font_name) 

% Change all fonts to font_name
FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);


% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,'plot_filename.pdf','-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,'plot_filename.pdf','-dpdf','-color','-landscape')
end


