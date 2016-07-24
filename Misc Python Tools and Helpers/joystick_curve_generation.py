#! /usr/bin/env python

###############################################################################
# joystick_curves.py
#
# script to generate curves for fitting joystick functions to desired shape
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 07/22/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
###############################################################################

import numpy as np
import matplotlib.pyplot as plt

# The data points to fit to
x = np.array([0, 1024, 2048, 3072, 4096])
y = np.array([-100, -25, 0, 25, 100])

# Cubic fit
fit_coeff = np.polyfit(x, y, 3)

# variable to hold the continuous curves for the fit
x_fit = np.linspace(0, 4096, 4097)
y_fit = fit_coeff[0] * x_fit**3 + fit_coeff[1] * x_fit**2 + fit_coeff[2] * x_fit + fit_coeff[3]


# Plot the results
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
plt.xlabel('X value', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('Y value', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(x, y, linestyle='', marker = 'o', label=r'Raw Datapoints')
plt.plot(x_fit, y_fit, linewidth=2, linestyle='-', label=r'Fit')

# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0,10)

# Create the legend, then fix the fontsize
leg = plt.legend(loc='upper right', ncol = 2, fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('plot_filename.pdf')

# show the figure
plt.show()



