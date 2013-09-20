function CRAWLAB_replot(figure)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% A function to take in a current MATLAB/Octave figure and 
%   make it look a little bit better. 
%   (a contrast the default MATLAB/Octave output)
%
% NOTE: Some work will still likely be needed.
%
% figure - format figure(X), where X is the figure you want to change
%            It should be already open.
%
% Usage: For open Figure 1... CRAWLAB_replot(figure(1))
%        You will be prompted to enter a base filename
%        File will be saved as a high-quality pdf
%
% The plot will probably look worse on screen. The saved version should be better.
%
% Created: 9/20/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu
%
% Modified: 
%   * 
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% get the figure that the user has passed in
h = figure;

% Decide if user is using MATLAB or Octave
% This will return a nonzero value if in Octave
isOctave = exist('OCTAVE_VERSION');

if isOctave == 0 % We're in MATLAB
    plot_line_width = 3;
    grid_line_width = 2;
else % We're in Octave
    plot_line_width = 8;
    grid_line_width = 4;
end

% Find all the lines in the current figure and change their width
plot_line = findobj(h, 'type', 'line');
set(plot_line,'LineWidth',plot_line_width)

% Set consistent font
font_name = 'Times New Roman';

% Define the papersize and margins
set (h,'papertype', '<custom>')
set (h,'paperunits','inches');

% papersize is 9" x 6" - 3x2 aspect ratio is best
set (h,'papersize',[9 6])       
set (h,'paperposition', [0,0,[9 6]])

% set the margins as percentage of page
set (gca,'position', [0.19, 0.19, 0.75, 0.75]) 

% Increase the axis font size to somethign readable
set (gca, 'fontsize', 24)

% Show a grid and set an appropriate line thickness 
grid on
set (gca, 'LineWidth',grid_line_width)

% Set the X and Y axis labels - Change their font sizes
x_label = get( gca,'Xlabel');  % get X label handle
set(x_label,'fontsize',28)
y_label = get( gca,'Ylabel');  % get Y label handle
set(y_label,'fontsize',28)


% Find the Legend and change the legend font
leg = findobj(h,'Type','axes','Tag','legend');
set (leg, 'FontSize', 20,'FontName',font_name) 

% Change all fonts to font_name
FN = findall(h,'-property','FontName');
set(FN,'FontName',font_name);

% Ask user for the desired filename to save
if isOctave == 0; % this is MATLAB
    beep(); % alert user that input is needed
    prompt = {'Enter desired base filename (.pdf will be added during save):'};
    dlg_title = 'Filename';
    num_lines = 1;
    def = {'plot_title'};
    base_filename = inputdlg(prompt,dlg_title,num_lines,def);
else    
    beep(); % alert user that input is needed
    base_filename = input(sprintf('\nEnter base filename (.pdf will be added during save): '),'s');
end

% Define the full filename
filename = strcat(base_filename,'.pdf');


% check if MATLAB or Octave to descide how to save
if isOctave == 0; % this is MATLAB
    % Save the figure as a high-res pdf
    print(h,filename{1},'-dpdf');
else
    % Save the figure as a high-res pdf
    print(h,filename,'-dpdf','-color','-landscape')
end


