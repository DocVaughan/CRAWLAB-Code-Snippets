#! /usr/bin/env python

###############################################################################
# pygame_Joystick_Basic.py
#
# script to read and process multiple axis of a gamepad for throttle and 
# steering inputs
#
# NOTE: As of 06/12/18, button numbers, etc are for Logitech F310 gamepad
#
# In one mode, when LB (left shoulder button) is held down, the left analog stick
# controls throttle and steering, up/down is throttle and left/right is steering
# 
# In the other mode, when RB (right shoulder button) is held down, the two
# analog sticks control the left and right throttle independently. The direction
# of those two throttle commands is controlled by the left/right motion of the pad.
#
# Output is printed to the screen as a pair of outputs:
#   Left throttle, left angle
#   Right throttle, right angle
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

# MAIN SCRIPT
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

        if joy.get_button(4): 
        # If LB is pressend, treat the input from the left analog stick
        # as throttle and steering
            left_throttle = VEL_SCALE * joy.get_axis(1)
            left_ang_vel = ROT_SCALE * joy.get_axis(0)
            
            # Match the right outputs to the left
            right_throttle, right_ang_vel = left_throttle, left_ang_vel

        elif joy.get_button(5): 
        # If RB if pressed, treat the two analog sticks independently
            left_throttle = VEL_SCALE * joy.get_axis(1)
            left_ang_vel = ROT_SCALE * joy.get_axis(0)
            
            right_throttle = VEL_SCALE * joy.get_axis(3)
            right_ang_vel = ROT_SCALE * joy.get_axis(2)
            
        else:
        # If neither is pressed, explicitly set all the velocities to 0
            left_throttle = 0
            left_ang_vel = 0
            right_throttle = 0
            right_ang_vel = 0

        # Now print out the current input. 
        print('\033[2J\033[;H')
        j = 15
        d = '.'
        print("Left".ljust(j, d), 'Throttle: {:+4.2f}    Steering: {:+4.2f}'.format(left_throttle, left_ang_vel))
        print("Right".ljust(j, d), 'Throttle: {:+4.2f}    Steering: {:+4.2f}'.format(right_throttle, right_ang_vel))

        # Sleep 0.1s between readings
        time.sleep(0.1)
# 
#     except utils.TimeoutError:
#         continue

    except KeyboardInterrupt:
        # Catches CTRL-C
        break

# Program terminated
print('Program finished, cleaning up...')
joy.quit()  

print('Cleanup successful, exiting...')
time.sleep(1)
sys.exit()  
