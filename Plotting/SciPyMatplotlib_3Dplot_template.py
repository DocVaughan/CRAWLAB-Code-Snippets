#! /usr/bin/env python 
##################################################################################
# A template to help create 3D figures with Matplotlib and Scipy
#
# It may actually look worse on screen. The saved version should be better.
# The 3D plots will likely need more changes to be presentable than 2D versions
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
#   * 
#
##################################################################################

import numpy as np
from matplotlib.pyplot import *             # Grab MATLAB plotting functions
from mpl_toolkits.mplot3d import Axes3D     # 3D plotting functions
from scipy.interpolate import griddata      # interpolate package's griddate function is better


# Example data so that code will show a plot... 
# It's best to remove and fill in your own
x = np.linspace(0, 5, 500)
y = np.linspace(np.pi/6,np.pi,10)

z = np.zeros_like

for ii in range(len(y)):
    z[ii] = 1.5 + np.sin(y[ii] * x)
    

# This function will take x and y arrays and create matrices from them
#   If X is shape (N,) or (N,1) and y is shape (M,) or (M,1), then 
#   x_grid and y_grid will be (M, N)
x_grid, y_grid = np.meshgrid(x, y)


heights = griddata((x, y),z,(x_grid, y_grid),method='nearest')

#-----  Copy from here down into your code, replacing items as needed ----------------
#   Many of these setting could also be made default by the .matplotlibrc file
fig = figure(figsize=(9,6))
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
ax = Axes3D(fig)
ax.view_init(20,-120)
setp(ax.get_ymajorticklabels(),family='CMUSerif-Roman',fontsize=18)
setp(ax.get_xmajorticklabels(),family='CMUSerif-Roman',fontsize=18)
setp(ax.get_zmajorticklabels(),family='CMUSerif-Roman',fontsize=18)

xLabel = ax.set_xlabel('X Label (units)',family='CMUSerif-Roman',fontsize=22,weight='bold')
yLabel = ax.set_ylabel('Y Label (units)',family='CMUSerif-Roman',fontsize=22,weight='bold')
zLabel = ax.set_zlabel('Z lable (unites)',family='CMUSerif-Roman',fontsize=22,weight='bold')

surf = ax.plot_surface(x_grid, y_grid, heights, linewidth=0, rstride=5, cstride=5, alpha=0.85,cmap=cm.bwr)
cset = ax.contourf(x_grid, y_grid, heights, zdir='z', offset= 0, cmap=cm.bwr)
# cset = ax.contour(x_grid, y_grid, heights, zdir='x', offset= np.max(x), cmap=cm.gray)
cset = ax.contour(x_grid, y_grid, heights, zdir='y', offset=1.5*np.max(y), cmap=cm.gray)

# Adjust the limits as necessary
# ax.set_xlim3d(0.0,0.5)
ax.set_ylim3d(0.0,1.5 * np.max(y))
ax.set_zlim3d(0.0,2.5)

# Adjust the axis ticks and their labels as necessary
# xticks([0,0.1,0.2,0.3,0.4,0.5])
# yticks([0.,0.04,0.08,0.12,0.16],['0','0.04','0.08','0.12',''])

# adjusts the padding around the 3D plot
ax.dist = 11

# Change the colorbar font
color_bar = colorbar(surf,shrink=0.5,aspect=8)
cbytick_obj = getp(color_bar.ax.axes, 'yticklabels')
setp(cbytick_obj, family='CMUSerif-Roman',fontsize=18)

# Export to svg for final edits in iDraw
# savefig('3D_plot.svg')
show()