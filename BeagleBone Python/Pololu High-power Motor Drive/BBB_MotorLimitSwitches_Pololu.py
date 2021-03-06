#! /usr/bin/env python

##########################################################################################
# BBB_MotorLimitSwitches.py
#
# Basic use of interrupts limit switches on the BeagleBone Black to start/stop 
# using the Pololu High-power motor driver - https://www.pololu.com/product/755
#
# Requires - Adafruit BeagleBone IO Python library
#
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 05/16/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

import time
import sys

class motor(object):
    """ Convenience class for controlling a Polulu High-Power Motor Driver
    
    Arguments
      DIRPin : the DIR pin 
      PWMpin : the PWM pin
      
    Other atributes
      isRunning : Boolean describing if motor is running or not
      speed : current speed of the motor
      direction : current direction the motor is running 
                  =None if the motor is not currently moving
                  
    """
    def __init__(self, DIRpin, PWMpin, PWMfreq = 2000):
        self.DIRpin = DIRpin
        self.PWMpin = PWMpin
        self.PWMfreq = PWMfreq
        self.isRunning = False
        self.currentDirection = None
        self.currentSpeed = 0
        
        # Set up the GPIO pins as output
        GPIO.setup(self.DIRpin, GPIO.OUT)


    def start(self, speed, direction):
        """ method to start a motor 
    
        Arguments:
          speed : speed of the motor 0-100 (as percentage of max)
          direction : CW or CCW, for clockwise or counterclockwise
        """
    
        # x01 and x02 have to be opposite to move, toggle to change direction
        if direction in ('cw','CW','clockwise'):
            GPIO.output(self.DIRpin, GPIO.LOW)
        elif direction in ('ccw','CCW','counterclockwise'):
            GPIO.output(self.DIRpin, GPIO.HIGH)
        else:
            raise ValueError('Please enter CW or CCW for direction.')
    
        # Start the motor
        # PWM.start(channel, duty, freq=2000, polarity=0)
        if 0 <= speed <= 100:
            PWM.start(self.PWMpin, speed, self.PWMfreq)
        else:
            raise ValueError("Please enter speed between 0 and 100, \
                              representing a percentage of the maximum \
                              motor speed.")

        # set the status attributes
        self.isRunning = True
        self.currentDirection = direction
        self.currentSpeed = speed

    def stop(self):
        """ Method to hard stop an individual motor"""
        
        PWM.set_duty_cycle(self.PWMpin, 0.0)
        
        # set the status attributes
        self.isRunning = False
        self.currentDirection = None
        self.currentSpeed = 0


    def set_speed(self, newSpeed):
        """ Method to change the speed of the motor, direciton is unchanged
        
        Arugments
          newSpeed : the desired new speed 0-100 (as percentage of max)
        """
        
        PWM.set_duty_cycle(self.PWMpin, newSpeed)
        self.currentSpeed = newSpeed


if __name__ == '__main__':
    # Demonstrates the use of this class

    # Set up the pins - These are mutable, but *don't* change them
    DIR_PIN = 'P8_8'        # DIR pin on board, controls direction
    PWM_PIN = 'P8_13'       # PWM pin on board, controls the speed of the motor 
    TOP_LIMIT = 'P8_12'     # Pin of top limit switch
    BOTTOM_LIMIT = 'P8_14'  # Pin of bottom limit switch


    # Create the motorA instance of the class
    motorA = motor(DIR_PIN, PWM_PIN)
    
    # GPIO P8_12 and P8_14switches
    GPIO.setup(TOP_LIMIT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.setup(BOTTOM_LIMIT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
  
    # now we'll define the threaded callback function  
    # this will run in another thread when our event is detected  
    def TOPlimit_callback(channel):  
        print 'Top limit reached.'
        motorA.stop()
        time.sleep(1)

    # now we'll define the threaded callback function  
    # this will run in another thread when our event is detected  
    def BOTTOMlimit_callback(channel):  
        print 'Bottom limit reached.'
        motorA.stop()
        time.sleep(1)


    # The GPIO.add_event_detect() line below set things up so that  
    # when a rising edge is detected, regardless of whatever   
    # else is happening in the program, the function 'my_callback' will be run  
    GPIO.add_event_detect(TOP_LIMIT, GPIO.RISING, callback=TOPlimit_callback, bouncetime=500)  
    GPIO.add_event_detect(BOTTOM_LIMIT, GPIO.RISING, callback=BOTTOMlimit_callback, bouncetime=500)   

    try:
        # Move down
        motorA.start(100, 'CW')
        time.sleep(0.5)

        while motorA.isRunning:
            # loop here until limit is reached
            print 'Moving down...'
            time.sleep(0.1)

        # Start Moving Motors Up
        time.sleep(1)
        motorA.start(100, 'CCW')
        time.sleep(0.5)
    
        while motorA.isRunning:
            # loop here until limit is reached
            print 'Moving up...'
            time.sleep(0.1)


    except KeyboardInterrupt:  
        motorA.stop()
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
    
    
    GPIO.cleanup()           # clean up GPIO on normal exit  