#! /usr/bin/env python

###############################################################################
# plotHeadingDuringTrajectory.py
#
# Test script to see to show the system heading during a trajectory by plotting
# a sprite or array every N points
#
# See https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.arrow.html for
# more info on arrow plotting. Specifically, if we aren't using axis('equal'), 
# then the arrow shape is affected by axes scaling. So, we might want to use
# annotate instead, as suggested.
#
# This example also includes using the annotate method.
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 05/04/20
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - @doc_vaughan
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

ARROW_EVERY_N = 10      # Plot a heading arrow every N data points

# How long should the arrow be. This is set so that we only see the arrow head
# and not any stem of it
ARROW_LENGTH = 0.135

# Define the "dummy" data. Is is one period of a circular trajectory in xy
t = np.linspace(0, 1, 101)
x_pos = np.sin(2 * np.pi * t)
y_pos = np.cos(2 * np.pi * t)

# Then, define the heading. Here, we pick a heading that should always point
# toward the center of the circle, plut some noise of +/-30deg
heading = -np.linspace(0, 2 * np.pi, 101) - np.pi/2 #+ np.pi/6 * np.sin(4 * np.pi * t)

# Using the heading, define the dx and dy points that define the direction
# of the arrow
dx_heading = ARROW_LENGTH * np.cos(heading)
dy_heading = ARROW_LENGTH * np.sin(heading)

# Alternately, we could (in this dummy dataset) set them to always be tangent
# to xy
# dx_heading = ARROW_LENGTH * np.cos(2 * np.pi * t)
# dy_heading = ARROW_LENGTH * -np.sin(2 * np.pi * t)


# ---------- Using plt.arrow ----------
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
plt.xlabel('X Displacement (m)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('Y Displacement (m)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(x_pos, y_pos, linewidth=2, linestyle='-', label=r'Trajectory')
# plt.plot(x2, y2, linewidth=2, linestyle='--', label=r'Data 2')
# plt.plot(x3, y3, linewidth=2, linestyle='-.', label=r'Data 3')
# plt.plot(x4, y4, linewidth=2, linestyle=':', label=r'Data 4')

for index, (x, y, dx, dy) in enumerate(zip(x_pos, y_pos, dx_heading, dy_heading)):

    if index % ARROW_EVERY_N == 0:
        plt.arrow(x - dx, y - dy, dx, dy, 
                  width=0.03, 
                  edgecolor=None,
                  length_includes_head=True, 
                  head_starts_at_zero=True, 
                  linewidth=0, # the edgecolor should take care of this?
                  overhang=0.0,
                  alpha=0.75,
                  zorder=1,)
        
# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0,10)

# Make the X and Y axis units per pixel equal 
# (so circles are circles in the plot)
plt.axis('equal')

# Create the legend, then fix the fontsize
# leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
# ltext  = leg.get_texts()
# plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('example_planarTrajectory_showing_heading.pdf')

# show the figure
# plt.show()



# ---------- Using ax.annotate ----------
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
plt.xlabel('X Displacement (m)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('Y Displacement (m)', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(x_pos, y_pos, linewidth=2, linestyle='-', label=r'Trajectory')
# plt.plot(x2, y2, linewidth=2, linestyle='--', label=r'Data 2')
# plt.plot(x3, y3, linewidth=2, linestyle='-.', label=r'Data 3')
# plt.plot(x4, y4, linewidth=2, linestyle=':', label=r'Data 4')

for index, (x, y, dx, dy) in enumerate(zip(x_pos, y_pos, dx_heading, dy_heading)):

    if index % ARROW_EVERY_N == 0:
        ax.annotate("",  # No text in this annotation, drawing arrow only
                    xycoords='data',        # Use the coordinates of the data
                    xy=(x+dx/2, y+dy/2),    # The start of the arrow
                    xytext=(x, y),          # The base of the arrow
                    arrowprops=dict(headwidth=10,
                                    headlength=15,
                                    edgecolor=None, 
                                    alpha=0.75,
                                    linewidth=0,
                                    zorder=1,))

# uncomment below and set limits if needed
# plt.xlim(0,5)
# plt.ylim(0,10)

# Make the X and Y axis units per pixel equal 
# (so circles are circles in the plot)
plt.axis('equal')

# Create the legend, then fix the fontsize
# leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
# ltext  = leg.get_texts()
# plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('example_planarTrajectory_showing_heading_annotate.pdf')

# show the figure
plt.show()

