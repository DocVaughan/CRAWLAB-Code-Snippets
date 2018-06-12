#! /usr/bin/env python

###############################################################################
# pygame_Joystick_Basic.py
#
# Basic reading of a joystick for throttle and steering inputs
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 06/12/18
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


import sys, time

# PyGame for joystick
# It's best to install via conda:
#  https://anaconda.org/cogsci/pygame
import pygame

# DEFINES
VEL_SCALE = -1.0
ROT_SCALE = 1.0
ACCEL = 2.0

# MAIN SCRIPT
#
pygame.init()

# Joystick connection
print('\nConnecting to joystick...')
if pygame.joystick.get_count() < 1:
    print('No joystick found, quitting')
    sys.exit(1)
else:
    joy = pygame.joystick.Joystick(0)
    joy.init()
print('Joystick found')

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                break
        if joy.get_button(0):
            print('axis 1 = {}, axis 2 = {}.'.format(VEL_SCALE*joy.get_axis(1),
                                                     ROT_SCALE*joy.get_axis(0)))
#       else:
#           print(0., 0.)
        time.sleep(0.1)

    except utils.TimeoutError:
        continue

    except KeyboardInterrupt:
        # Catches CTRL-C
        break

# Program terminated
print('Program finished, cleaning up...')
joy.quit()  

print('Cleanup successful, exiting...')
time.sleep(1)
sys.exit()  
