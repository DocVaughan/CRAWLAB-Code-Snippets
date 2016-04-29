#! /usr/bin/env python

###############################################################################
# ZVshapingBasic_wrapping.py
#
# Python code to wrap a very simple shared library
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/27/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 04/29/16 - JEV - joshua.vaughan@louisiana.edu
#       - corrected the return type, int is returned by default, needed float
#       - C buffer is retained between calls, so we need to clear each time
#       - better commenting
#
###############################################################################

import numpy as np
import matplotlib.pyplot as plt

# Import the ctypes module. Importing all for now.
from ctypes import *

# Load the libhello_world c code, built as a shared-library
# Give it a name to make it callable
# Currently, requires the file to be in the path/folder this script is run from
zv_shaping = CDLL('libZVshapingBasic.dylib')

# define the argument and return types (not always necessary, it seems)
zv_shaping.doZVShaping.argtypes = [c_float]
zv_shaping.doZVShaping.restype = c_float # int is assumed if not specified


# Set up an unshaped input to feed into the C function doing the shaping
# Just a step input of 1 unit at t=0 for now
t = np.linspace(0, 3, 301)
U = 1.0 * np.ones_like(t)
shaped = np.zeros_like(t)

# First pass through the array with 0 input. Currently, the C array is static,
# meaning that it is maintained between function calls. This is done to make
# real-time implementation easier, but requires this step to work properly 
# for array-based simluations/calculations like these.
for index, input in enumerate(U):
    shaped[index] = zv_shaping.doZVShaping(0)


# We're not trying to pass an array to C yet, 
# so we have to loop through the unshaped input
for index, input in enumerate(U):
    shaped[index] = zv_shaping.doZVShaping(input)


# Now's let's plot the command that has been shaped by the doZVShaping C func.

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
plt.xlabel('Time (s)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('Command', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(t, U, linewidth=2, linestyle='--', label=r'Unshaped')
plt.plot(t, shaped, linewidth=2, linestyle='-', label=r'ZV Shaped')

# uncomment below and set limits if needed
# plt.xlim(0,5)
plt.ylim(0, 1.25)

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
