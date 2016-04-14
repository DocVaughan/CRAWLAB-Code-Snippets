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

import numpy as np
import matplotlib.pyplot as plt


# Make the figure pretty, then plot the results
#   "pretty" parameters selected based on pdf output, not screen output
#   Many of these setting could also be made default by the .matplotlibrc file

# Example data so that code will show a plot... 
# It's best to remove and fill in your own
x1 = np.linspace(0, 5, 501)
x2 = x1
x3 = x1
x4 = x1

y1 = sin(x1)
y2 = 0.5*sin(x2)
y3 = 0.75*sin(x3)
y4 = 1.25*sin(x4)


#-----  Copy from here down into your code, replacing items as needed ----------------

# Set the plot size - 3x2 aspect ratio is best
fig = plt.figure(figsize=(6,4))
ax = plt.gca()
plt.subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

# Change the axis units font
plt.setp(ax.get_ymajorticklabels(),fontsize=18)
plt.setp(ax.get_xmajorticklabels(),fontsize=18)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Turn on the plot grid and set appropriate linestyle and color
ax.grid(True,linestyle=':', color='0.75')
ax.set_axisbelow(True)

# Define the X and Y axis labels
plt.xlabel('X label (units)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('Y label (units)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(x1, y1, linewidth=2, linestyle='-', label=r'Data 1')
plt.plot(x2, y2, linewidth=2, linestyle='--', label=r'Data 2')
plt.plot(x3, y3, linewidth=2, linestyle='-.', label=r'Data 3')
plt.plot(x4, y4, linewidth=2, linestyle=':', label=r'Data 4')

# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0,10)

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('plot_filename.pdf')

# show the figure
plt.show()
