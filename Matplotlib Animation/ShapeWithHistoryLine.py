#! /usr/bin/env python

##########################################################################################
# Script to animate an example move

#
# Created: 09/29/14
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import numpy as np                      # Grab all of the NumPy functions
from matplotlib import pyplot as plt    # Grab MATLAB plotting functions
import matplotlib.animation as animation

import matplotlib as mpl
mpl.rcParams['savefig.dpi']=160


# Define the example path
x = np.sin(2*np.pi*np.linspace(0,5,150))
y = np.cos(2*np.pi*np.linspace(0,5,150)) + 0.25*np.random.random(150)

# Set up basic Figure Properties
#   Many of these setting could also be made default by the .matplotlibrc file
#   axes limits may need to be adjusted depending on input
fig = plt.figure(figsize=(8,4.5))
# fig = plt.figure(figsize=(6,4))
ax = plt.gca()
plt.subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
plt.setp(ax.get_ymajorticklabels(),family='CMUSerif-Roman',fontsize=18)
plt.setp(ax.get_xmajorticklabels(),family='CMUSerif-Roman',fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

plt.xlabel(r'Position (m)',family='CMUSerif-Roman',fontsize=22,weight='bold',labelpad=5)
plt.ylabel(r'Position (m)',family='CMUSerif-Roman',fontsize=22,weight='bold',labelpad=10)


# For the trapezoid
plt.ylim(-2.0,2.0)
plt.xlim(-2.0,2.0)


historyLine, = plt.plot([],[],linewidth=2,linestyle = '--', label='History')
shape = plt.Circle(([],[]),0.1,ec='none')


leg = plt.legend(loc='upper right', fancybox=True)
ltext  = leg.get_texts()
plt.setp(ltext,family='CMUSerif-Roman',fontsize=16)



def init():
    historyLine.set_data([],[])
    shape.center = (x[0],y[0])
    ax.add_patch(shape)
    return historyLine, shape


def animate(i):
    print 'Processing frame {}.'.format(i)
    shape.center = (x[i],y[i])
    historyLine.set_data(x[0:i],y[0:i])


    return historyLine, shape,

ani = animation.FuncAnimation(fig, animate, frames=5, init_func=init)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
ani.save('simple_animaiton.mov', fps=5)

plt.show()