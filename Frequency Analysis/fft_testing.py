#! /usr/bin/env python

###############################################################################
# fft_testing.py
#
# Script to test updated NumPy FFT algorithms
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 08/05/20
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
from numpy.fft import rfft, rfftfreq

# Set up the test data
dt = 0.01                       # Sample time (s)
t = np.arange(0,10 + dt, dt)

f1 = 1.0 * 2.0 * np.pi  # 1 Hz
f2 = 3.4 * 2.0 * np.pi  # 3.4 Hz
f3 = 30.0 * 2.0 * np.pi

data =  np.sin(f1 * t) + np.sin(f2 * t) + np.sin(f3 * t)
num_samples = len(data)

fft_mag = np.abs(rfft(data))
fft_freq = rfftfreq(num_samples, dt)

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
plt.xlabel('Frequency (Hz)', fontsize=22, weight='bold', labelpad=5)
plt.ylabel('FFT Magnitude', fontsize=22, weight='bold', labelpad=10)
 
plt.plot(fft_freq, fft_mag, linewidth=2, linestyle='-', label=r'Data 1')

# uncomment below and set limits if needed
plt.xlim(0, 50)
# plt.ylim(0,10)

# Create the legend, then fix the fontsize
# leg = plt.legend(loc='upper right', ncol = 1, fancybox=True)
# ltext  = leg.get_texts()
# plt.setp(ltext,fontsize=18)

# Adjust the page layout filling the page using the new tight_layout command
plt.tight_layout(pad=0.5)

# save the figure as a high-res pdf in the current folder
# plt.savefig('plot_filename.pdf')

# show the figure
plt.show()

