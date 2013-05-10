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
%   - the axis labels - be sure to include units
%   - the legend labels
%   - the filename to save the figure as
%
% Created: 4/19/13 - Joshua Vaughan (joshua.vaughan@louisiana.edu)
%
% Modified: 
%   * 
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Example data so that code will show a plot... 
x1 = 0:0.01:5;
x2 = x1;
x3 = x1;
x4 = x1;

y1 = sin(x1);
y2 = 0.5*sin(x2);
y3 = 0.75*sin(x3);
y4 = 1.25*sin(x4);


%-----  Copy from here down into your code, replacing items as needed ----------------
%
%  The plot is formatted for saving, so it might be ugly on screen
h = figure

% Define the papersize and margins
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');

% papersize is 9" x 6" - 3x2 aspect ratio is best
set (h,'papersize',[9 6])       
set (h,'paperposition', [0,0,[9 6]])

% set the margins as percentage of page
set (gca,'position', [0.19, 0.19, 0.75, 0.75]) 

% Increase the axis font size to somethign readable
set (gca, "fontsize", 24)

% Change all fonts to CMU Serif
FN = findall(h,'-property','FontName');
set(FN,'FontName','CMU Serif');

% This is the actual plotting... Change xi and yi
plot(x1,y1,'LineWidth',6,x2,y2,'--','LineWidth',6,x3,y3,'-.','LineWidth',6,x4,y4,':','LineWidth',6)

% Show a grid and set an appropriate line thickness 
grid on
set (gca, 'LineWidth',4)

% Set the X and Y axis labels - Change these to suit your plot
xlabel('X Label (units)','fontsize',28)
ylabel('Y Label (units)','fontsize',28)

% Create the legend - change 'Data i' to suit your plot
leg = legend('Data 1','Data 2','Data 3','Data 4')
set (leg, "FontSize", 20,'FontName','CMU Serif') 

% Save the figure as a high-res pdf
print(h,'plot_filename.pdf','-dpdf','-color','-landscape')

