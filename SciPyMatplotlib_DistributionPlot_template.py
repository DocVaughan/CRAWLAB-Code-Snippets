#! /usr/bin/env python 

from numpy import *    
import scipy
from matplotlib.pyplot import * # Grab MATLAB plotting functions
from scipy.integrate import odeint


# The data
categories = [10,30,50,70,90] # [Group 1, Group 2, Group 3, Group 4, Group 5]
occurences = [1,5,13,6,5]

# Plot the response#   Many of these setting could also be made default by the .matplotlibrc file
fig = figure(figsize=(6,4))
ax = gca()
subplots_adjust(bottom=0.2,left=0.12,top=0.96,right=0.96)
setp(ax.get_ymajorticklabels(),family='CMU Serif',fontsize=18)
setp(ax.get_xmajorticklabels(),family='CMU Serif',fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

xlabel(r'Categories',family='CMU Serif',fontsize=22,weight='bold',labelpad=5)
ylabel(r'Occurences',family='CMU Serif',fontsize=22,weight='bold',labelpad=8)


bar(categories,occurences,width=15, align='center')

xticks([10,30,50,70,90],['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5'])

# Uncomment below to add a legend if necesssary
# leg = legend(loc='upper right', fancybox=True)
# ltext  = leg.get_texts() 
# setp(ltext,family='CMU Serif',fontsize=16)

# save the figure as a high-res pdf in the current folder
# savefig('Distribution_Template.pdf',dpi=600)

# save the figure as a svg, for editing in a vector graphics program
# savefig('Distribution_Template.svg')


# show the figure
show()