#! /usr/bin/env python 
#! /usr/bin/env python

###############################################################################
# matplotlib_DistributionPlot_template.py
#
# template for bar/distributions plots in matplotlib
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/14/16
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

# The data
categories = [10, 30, 50, 70, 90] # [Group 1, Group 2, Group 3, Group 4, Group 5]
occurences = [1, 5, 13, 6, 5]

# Plot the data
# Many of these setting could also be made default by the .matplotlibrc file
fig = plt.figure(figsize=(6,4))
ax = plt.gca()
plt.subplots_adjust(bottom=0.2,left=0.12,top=0.96,right=0.96)
plt.setp(ax.get_ymajorticklabels(),family='serif',fontsize=18)
plt.setp(ax.get_xmajorticklabels(),family='serif',fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

plt.xlabel(r'Categories', family='serif', fontsize=22, weight='bold', labelpad=5)
plt.ylabel(r'Occurences', family='serif', fontsize=22, weight='bold', labelpad=8)

plt.bar(categories, occurences, width=15, align='center')

plt.xticks([10,30,50,70,90], ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5'])

# Uncomment below to rotate the labels to be vertical, if needed
# plt.setp(ax.get_xmajorticklabels(), rotation=90)

# Uncomment below to add a legend if necessary
# leg = plt.legend(loc='upper right', fancybox=True)
# ltext  = leg.get_texts() 
# plt.setp(ltext,family='serif',fontsize=16)

# save the figure as a high-res pdf in the current folder
# plt.savefig('Distribution_Template.pdf', dpi=600)

# save the figure as a svg, for editing in a vector graphics program
# plt.savefig('Distribution_Template.svg')


# show the figure
plt.show()