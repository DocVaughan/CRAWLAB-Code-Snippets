#! /usr/bin/env python

##########################################################################################
# calc_doublePendulumFreq.py
#
# script to calculate the linearized frequencies for a double-pendulum
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/22/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import numpy as np
import matplotlib.pyplot as plt

def calc_doublePendulumFreq(mh, mp, l1, l2, g = 9.81):
    """ 
    Function to calculate the linearized frequencies of a double-pendulum
    
    Arguments:
      mh : mass of the hook (kg)
      mp : mass of the payload (kg)
      l1 : supension cable length (m)
      l2 : rigging length (m)
      g : gravitation acceleration (9.81 m/s^2 is default, we're on Earth)
      
    Returns:
      The two natural frequencies (rad/s)
    
    """
    R = mp / mh

    beta = np.sqrt((1 + R)**2 * (1.0/l1 + 1.0/l2)**2 - 4 * ((1.0 + R) / (l1 * l2)))
    
    w1 = np.sqrt(g / 2) * np.sqrt((1+R) * (1.0/l1 + 1.0/l2) - beta)
    w2 = np.sqrt(g / 2) * np.sqrt((1+R) * (1.0/l1 + 1.0/l2) + beta)
    
    return w1, w2


if __name__ == '__main__':
    # Define system parameters
    mh = 50.0           # mass of the hook (kg)
    mp = 22.7/2           # mass of the payload (kg)
    l1 = 3.5            # suspension cable length (m)
    l2 = 1.8            # rigging length (m)

    w1, w2 = calc_doublePendulumFreq(mh, mp, l1, l2)
    
    print 'The natrual frequencies are {:0.4f} rad/s and {:0.4f} rad/s.'.format(w1, w2)
    print 'The natrual frequencies are {:0.4f} Hz and {:0.4f} Hz.'.format(w1/(2*np.pi), w2/(2*np.pi))
    
    
    # We can also look at a range of payload masses
    mp = np.arange(10, 50, 1)
    
    w1, w2 = calc_doublePendulumFreq(mh, mp, l1, l2)
    
    # Set the plot size - 3x2 aspect ratio is best
    fig = plt.figure(figsize=(6,4))
    ax = plt.gca()
    plt.subplots_adjust(bottom=0.17, left=0.17, top=0.96, right=0.96)

    # Change the axis units to CMUSerif-Roman
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
    plt.xlabel('Payload Mass (kg)', fontsize=22, weight='bold', labelpad=5)
    plt.ylabel('Frequency (Hz)', fontsize=22, weight='bold', labelpad=10)
 
    plt.plot(mp, w1 / (2*np.pi), linewidth=2, linestyle="-", label=r'$\omega_1$')
    plt.plot(mp, w2 / (2*np.pi), linewidth=2, linestyle="--", label=r'$\omega_2$')

    # uncomment below and set limits if needed
    # plt.xlim(0,5)
    plt.ylim(0,0.75)

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
