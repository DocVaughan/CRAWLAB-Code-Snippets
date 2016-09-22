#! /usr/bin/env python 
##################################################################################
# matplotlib_SurfacePlot_template.py
# 
# A template to help create surface plots with Matplotlib and Scipy
#
# It may actually look worse on screen. The saved version should be better.
# The 3D plots will likely need more changes to be presentable than 2D versions
#
# See http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html for more info
#
# This will not do anyting on it's own. Copy and paste into your script, then...
#
# You will have to fill in:
#   - the actual things to plot
#   - the axis labels - be sure to include units
#   - the legend labels
#   - the filename to save the figure as
#
# Created: 05/19/14 - Joshua Vaughan (joshua.vaughan@louisiana.edu)
#
# Modified: 
#   * 09/21/16 - JEV - joshua.vaughan@louisiana.edu
#       - update to import matplotlib.pyplot as plt style import
#       - better commenting and general cleanup
#
##################################################################################

import numpy as np
import matplotlib.pyplot as plt             # Grab MATLAB plotting functions
from mpl_toolkits.mplot3d import Axes3D     # 3D plotting functions
from scipy.interpolate import griddata      # interpolate package's griddate function is better


# Example data so that code will show a plot... 
# It's best to remove and fill in your own

# Create the arrays for the x and y data
x = np.arange(-5, 5, 0.25)
y = np.arange(-5, 5, 0.25)

# This function will take x and y arrays and create matrices from them
#   If X is shape (N,) or (N,1) and y is shape (M,) or (M,1), then 
#   x_grid and y_grid will be (M, N)
x_grid, y_grid = np.meshgrid(x, y)

# In NumPy, we can pass the grid variables to functions. This will create a
# properly sized matrix for surface plotting
heights = np.sin(np.sqrt(x_grid**2 + y_grid**2))

#-----  Copy from here down into your code, replacing items as needed ----------------
#   Many of these setting could also be made default by the .matplotlibrc file
fig = plt.figure(figsize=(9,6))
plt.subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
ax = Axes3D(fig)
ax.view_init(20,-120)
plt.setp(ax.get_ymajorticklabels(), fontsize=18)
plt.setp(ax.get_xmajorticklabels(), fontsize=18)
plt.setp(ax.get_zmajorticklabels(), fontsize=18)

xLabel = ax.set_xlabel('X Label (units)', fontsize=22, weight='bold')
yLabel = ax.set_ylabel('Y Label (units)', fontsize=22, weight='bold')
zLabel = ax.set_zlabel('Z Label (units)', fontsize=22, weight='bold')

surf = ax.plot_surface(x_grid, y_grid, heights, linewidth=0, rstride=1, cstride=1, alpha=0.85, cmap=plt.cm.bwr)
cset = ax.contourf(x_grid, y_grid, heights, zdir='z', offset= -2, cmap=plt.cm.bwr)
# cset = ax.contour(x_grid, y_grid, heights, zdir='x', offset= np.max(x), cmap=cm.gray)
cset = ax.contour(x_grid, y_grid, heights, zdir='y', offset=1.25*np.max(y), cmap=plt.cm.gray)

# Adjust the limits as necessary
ax.set_xlim3d(-1.25 * np.max(x), 1.25 * np.max(x))
ax.set_ylim3d(-1.25 * np.max(y), 1.25 * np.max(y))
ax.set_zlim3d(-2.0, 1.01)


# Adjust the axis ticks and their labels as necessary
# xticks([0,0.1,0.2,0.3,0.4,0.5])
# yticks([0.,0.04,0.08,0.12,0.16],['0','0.04','0.08','0.12',''])

# adjusts the padding around the 3D plot
ax.dist = 11

# Change the colorbar font
color_bar = plt.colorbar(surf,shrink=0.5,aspect=8)
cbytick_obj = plt.getp(color_bar.ax.axes, 'yticklabels')
plt.setp(cbytick_obj,  fontsize=18)

# Export to svg for final edits in iDraw/Graphic
# plt.savefig('3D_plot.svg')
plt.show()