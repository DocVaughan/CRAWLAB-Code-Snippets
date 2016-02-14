#! /usr/bin/env python

###############################################################################
# dual_y_axes.py
#
# Plotting with two y-axes, sharing the same x-axes
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# TODO: The ax2 gridlines are "above" the ax1 plots. Need to correct this.
#
# Created: 02/13/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

import numpy as np
import matplotlib.pyplot as plt

# Set up the date
x = np.linspace(0, 5, 501)
y1 = np.sin(x)
y2 = 5 + np.cos(x)

fig = plt.figure(figsize=(6,4))
ax1 = plt.gca()
plt.subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

# Change the axis units font
plt.setp(ax1.get_ymajorticklabels(),fontsize=18)
plt.setp(ax1.get_xmajorticklabels(),fontsize=18)

# Remove the top and right border, they are not needed
ax1.spines['right'].set_color('none')
ax1.spines['top'].set_color('none')

# Define the positions of the axes tick marks
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')

# Manually set the x-axis limits, if necessary
# plt.xlim(0,5)

# Turn on the plot grid and set appropriate linestyle and color
ax1.grid(True, linestyle=':', color='0.75')
ax1.set_axisbelow(True)

# Define the X and Y1 axis labels
ax1.set_xlabel('X-Label (units)', fontsize=22, weight='bold', labelpad=5)
ax1.set_ylabel(r'$y_1$ Label (units)', fontsize=22, weight='bold', labelpad=10)

# Plots gain used on input to tracking of Surge
ax1.plot(x, y1, linewidth=2, linestyle='-', label=r'$y_1$', )

# Manually set the y1-axes limits, if necessary
ax1.set_ylim(-4, 4)


# Set up the 2nd Y-axis, using the same x-axis as the first
ax2 = ax1.twinx()

# Remove the top border, it's not needed
ax2.spines['top'].set_color('none')

# Turn on the plot grid and set appropriate linestyle and color
ax2.grid(True, linestyle=':', color='0.75')
ax2.set_axisbelow(True) 

# Change the y2 axis units font
plt.setp(ax2.get_ymajorticklabels(), fontsize=18)

# Define the Y2 axis labels
ax2.set_ylabel(r'$y_2$ Label (units)', fontsize=22, weight='bold', labelpad=10)

ax2.plot(x, y2, linewidth=2, linestyle='--', color = '#377eb8', label=r'$y_2$')

# Manually set the y2-axes limits, if necessary
ax2.set_ylim(0, 8)

# Create the legend, then fix the fontsize
# ask matplotlib for the plotted objects and their labels
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
leg = ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right', ncol = 1, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
plt.savefig('dual_yAxes_plot.pdf')

# show the figure
plt.show()
