#! /usr/bin/env python

###############################################################################
# pygame_Joystick_Basic.py
#
# Basic reading of a joystick for throttle and steering inputs. On a PS4 
# controller, the square button will act as the deadman's witch and the left
# analog stick will control throttle and steering. In other words, hold the 
# square to start sending commands, then use the left analog stick to drive.
#
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
import pygame

# Constants
VEL_SCALE = -1.0
ROT_SCALE = 1.0
ACCEL = 2.0

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
            print('axis 1 = {:+.2f} \t axis 2 = {:+.2f}.'.format(VEL_SCALE * joy.get_axis(1),
                                                                 ROT_SCALE * joy.get_axis(0)))

        time.sleep(0.1)

#     except utils.TimeoutError:
#         continue

    except (KeyboardInterrupt, SystemExit):
        # Catches CTRL-C
        break

# Program terminated
print('Program finished, cleaning up...')
joy.quit()  

print('Cleanup successful, exiting...')
time.sleep(1)
sys.exit()  
