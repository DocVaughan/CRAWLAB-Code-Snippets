#! /usr/bin/env python

###############################################################################
# main.py
#
# Simple Knight Rider effect using a neopixel strip connected to an esp32. Intended to be
# used to indicate the status of a system.
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 02/03/19
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

import machine 
import neopixel
import time

NEO_PIN = 15
NUM_LEDS = 60
NUM_CYCLE = 5

RED_HIGH = (255,0,0)
RED_LOW = (16,0,0)
GREEN_HIGH = (0,255,0)
GREEN_LOW = (0,16,0)
BLUE_HIGH = (0,0,255)
BLUE_LOW = (0,0,16)
YELLOW_HIGH = (255,128,0)
YELLOW_LOW = (16,8,0)

color_dict = {'red': {'high':RED_HIGH, 'low':RED_LOW},
              'green': {'high':GREEN_HIGH, 'low':GREEN_LOW},
              'blue': {'high':BLUE_HIGH, 'low':BLUE_LOW},
              'yellow': {'high':YELLOW_HIGH, 'low':YELLOW_LOW}}


class neo_status():
    def __init__(self, neo_pin = NEO_PIN, 
                       number_of_leds = NUM_LEDS, 
                       led_in_cycle = NUM_CYCLE,
                       color = 'red'):

        self.neo_pin = neo_pin 
        self.number_of_leds = number_of_leds
        self.led_in_cycle = led_in_cycle
        self.color = color

        self.neo = neopixel.NeoPixel(machine.Pin(self.neo_pin), self.number_of_leds)

        # Should be filled with 0s to start (off), but ensure that's true
        self.neo.fill((0,0,0))
        self.neo.write()


    def status_cycle(self, color):
        """ 
        Cycle a bright section of LED back and forth over a dimmer section of the same
        color. This currently (as of 02/03/19) blocks indefinitely.
        
        Arguments
            color : 'red', 'green', 'yellow', or 'blue'
        """
        
        if color not in ('red','green','yellow','blue'):
            print('Please choose the color to be \'red\', \'green\', \'yellow\', or \'blue\'.')
            return

        index = 0
        going = True
        self.color = color

        try:
            while(True):
                # Fill with low brightness
                self.neo.fill(color_dict[self.color]['low'])

                if (index + self.led_in_cycle >= self.number_of_leds):
                    going = False
         
                elif (index <= 0):
                    going = True


                if going:
                    for n in range(self.led_in_cycle):
                        self.neo[index + n] = color_dict[self.color]['high']
        
                    index = index + 1

                else:
                    for n in range(self.led_in_cycle):
                        self.neo[index + self.led_in_cycle - n - 1] = color_dict[self.color]['high']

                    index = index - 1

                self.neo.write()

                time.sleep(0.01)

        except (KeyboardInterrupt):
            # If interrupt manually with control-C, turn all the LEDs off
            self.turn_all_off()


    def turn_all_off(self):
        """ Turn off all LEDs"""
        self.neo.fill((0,0,0))
        self.neo.write()


    def turn_all_to_color(self, color, brightness = 1):
        """ Turn all LEDs on the strip to a color
        
        Arguments:
            color : can be 'red', 'green', 'yellow', 'blue', 
                    or a tuple of (r,g,b) where r, g, and b are between 0 and 255
            brightness : between 0 and 1, 0 is off, 1 is full brightness
        """
        
        if color in ('red','green','yellow','blue'):
            if brightness > 1:
                brightness = 1
            elif brightness < 0:
                brightness = 0
            
            self.color = color
            color_tuple = [int(x*brightness) for x in color_dict[self.color]['high']]
            
            self.neo.fill(color_tuple)
            self.neo.write()
        
        else:
            # TODO: Check that the color tuple is valid
            self.neo.fill(color)
            self.neo.write()


    def blink_all(self, color, number_of_blinks, brightness=1):
        """ Blink the entire stand at 2Hz number_of_blinks times
        
        Arguments:
            color : can be 'red', 'green', 'blue', 
                    or a tuple of (r,g,b) where r, g, and b are between 0 and 255
            number_of_blinks : integer number of times to blink
            brightness : between 0 and 1, 0 is off, 1 is full brightness
        """
        
        for _ in range(number_of_blinks):
            self.turn_all_to_color(color, brightness)
            time.sleep(0.25)
            self.turn_all_off()
            time.sleep(0.25)


    def blink_all_timed(self, color, blink_duration, brightness=1):
        """ Blink the entire stand at 2Hz for blink_duration, turns off afterwards
        
        Arguments:
            color : can be 'red', 'green', 'blue', 
                    or a tuple of (r,g,b) where r, g, and b are between 0 and 255
            blink_duration : duration to blink for in seconds
            brightness : between 0 and 1, 0 is off, 1 is full brightness
        """
        start_time = time.ticks_ms()
        
        run_time = time.ticks_diff(time.ticks_ms(), start_time) 
        
        while run_time/1000 < blink_duration:
            if run_time % 500 < 250: 
                self.turn_all_to_color(color, brightness)
            else:
                self.turn_all_off()
            
            time.sleep_ms(1)
            run_time = time.ticks_diff(time.ticks_ms(), start_time) 

        # Ensure that all are off 
        self.turn_all_off()
        