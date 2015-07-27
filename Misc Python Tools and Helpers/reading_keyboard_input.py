#!/usr/bin/env python

#! /usr/bin/env python

##########################################################################################
# reading_keyboard_input.py
#
# Reads keyboard input using either the readchar or pygame modules
# Just prints the key pressed if it matches a choice
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 07/27/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

from __future__ import print_function

import os
import readchar

#os.environ['SDL_VIDEODRIVER'] = 'dummy' #supposed to trick pygame into thinking a display has been opened
import pygame
pygame.init()
pygame.display.set_mode((1,1))
clock = pygame.time.Clock()

USE_READCHAR = False     # True to use readchar, false to use pygame

def read_keys():
    SHUTDOWN = False
    
    while not SHUTDOWN:

        if USE_READCHAR:

            # get the next pressed character
            # This is a blocking call
            pressed_key = readchar.readkey()
            
            #long link commands
            if pressed_key == 'q':
                print('long link forward rotation')
            
            if pressed_key == 'a':
                print('long link backward rotation')

            #short link commmands
            if pressed_key == 'w':
                print('short link forward rotation')
            
            if pressed_key == 's':
                print('short link backward rotation') 
        
            # gripper commands   
            if pressed_key == 'e':
              print('gripper forward rotation')
            
            if pressed_key == 'd':
              print('gripper backward rotation')
        
            if pressed_key == 'f':
                print('Shutting down...')
                SHUTDOWN = True
        
        else: # Use pygame
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                      print('long link forward rotation')

                    if event.key == pygame.K_a:
                      print('long link backward rotation')
            
                    if event.key == pygame.K_w:
                      print('short link forward rotation')
            
                    if event.key == pygame.K_s:
                      print('short link backward rotation')
            
                    if event.key == pygame.K_e:
                      print('gripper forward rotation')
            
                    if event.key == pygame.K_d:
                      print('gripper backward rotation')
                      
                    if event.key == pygame.K_f:
                        print('Shutting down...')
                        SHUTDOWN = True
                      
    clock.tick(60)  # 60 fps


if __name__ == '__main__':
    try:
        read_keys()

    except (KeyboardInterrupt, SystemExit):
        print('\nExiting...')
