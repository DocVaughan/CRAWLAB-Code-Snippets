#!/usr/bin/env python

###############################################################
#
# talker.py
#
# This program uses ROSS to send a command to a listener node which will move a dynamixel servo.
#
# Created 21 July, 2015
#   -Matthew Begneaud
#
# References:
# -This program borrows formatting from the tutorials found at: wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29
#
#Below is their required license and Copyright information:
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# 'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

###############################################################

from __future__ import print_function

import os
import readchar

#os.environ['SDL_VIDEODRIVER'] = 'dummy' #supposed to trick pygame into thinking a display has been opened
import pygame
pygame.init()
pygame.display.set_mode((1,1))
clock = pygame.time.Clock()

USE_READCHAR = False     # True to use readchar, false to use pygame

def talker():
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
        talker()

    except (KeyboardInterrupt, SystemExit):
        print('\nExiting...')
