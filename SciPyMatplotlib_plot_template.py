#! /usr/bin/env python 
##################################################################################
# A template to help create readable figures with Matplotlib and Scipy
#
# It may actually look worse on screen. The saved version should be better.
#
# This will not do anyting on it's own. Copy and paste into your script, then...
#
# You will have to fill in:
#   - the actual things to plot
#   - the axis labels - be sure to include units
#   - the legend labels
#   - the filename to save the figure as
#
# Created: 4/19/13 - Joshua Vaughan (joshua.vaughan@louisiana.edu)
#
# Modified: 
#   * 
#
##################################################################################

from matplotlib.pyplot import * # Import the plotting functions


# Make the figure pretty, then plot the results
#   "pretty" parameters selected based on pdf output, not screen output
#   Many of these setting could also be made default by the .matplotlibrc file

# Example data so that code will show a plot... 
# It's best to remove and fill in your own
x1 = r_[0:5:500j]
x2 = x1
x3 = x1
x4 = x1

y1 = sin(x1)
y2 = 0.5*sin(x2)
y3 = 0.75*sin(x3)
y4 = 1.25*sin(x4)

#-----  Copy from here down into your code, replacing items as needed ----------------
#
# Set the plot size - 3x2 aspect ratio is best
fig = figure(figsize=(6,4))
ax = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)

# Change the axis units to CMU Serif
setp(ax.get_ymajorticklabels(),family='CMU Serif',fontsize=18)
setp(ax.get_xmajorticklabels(),family='CMU Serif',fontsize=18)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Turn on the plot grid and set appropriate linestyle and color
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

# Define the X and Y axis labels
xlabel('X label (units)',family='CMU Serif',fontsize=22,weight='bold',labelpad=5)
ylabel('Y label (units)',family='CMU Serif',fontsize=22,weight='bold',labelpad=10)

plot(x1,y1,linewidth=2,label=r'Data 1')
plot(x2,y2,linewidth=2,linestyle="--",label=r'Data 2')
plot(x3,y3,linewidth=2,linestyle="-.",label=r'Data 3')
plot(x4,y4,linewidth=2,linestyle=":",label=r'Data 4')

# uncomment below and set limits if needed
# xlim(0,5)
# ylim(0,10)

# Create the legend, then fix the fontsize
leg = legend(loc='upper right', fancybox=True)
ltext  = leg.get_texts() 
setp(ltext,family='CMU Serif',fontsize=16)

# save the figure as a high-res pdf in the current folder
savefig('plot_filename.pdf',dpi=600)

# show the figure
show()
