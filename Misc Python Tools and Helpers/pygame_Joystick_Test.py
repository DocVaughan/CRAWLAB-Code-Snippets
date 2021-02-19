#! /usr/bin/env python

###############################################################################
# pygame_Joystick_Test.py
#
# Script to read all the buttons from a joystick using pygame. 
# Data is output using a pygame window.
# 
# Code is modified from that in the pygame tutorial, whose preamble is copied 
# below.
#
# Created: 04/26/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - @doc_vaughan
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 02/19/21 - Some cleanup trying to make closing/exit more elegant.
#
# TODO:
#   * 02/19/21 - further cleanup of exit when running from IPython
###############################################################################

"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
Show everything we can pull off the joystick
"""
import pygame
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
class TextPrint(object):
    """
    This is a simple class that will help us print to the screen
    It has nothing to do with the joysticks, just outputting the
    information.
    """
    def __init__(self):
        """ Constructor """
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)
 
    def pg_print(self, my_screen, text_string):
        """ Draw text onto the screen. """
        text_bitmap = self.font.render(text_string, True, BLACK)
        my_screen.blit(text_bitmap, [self.x_pos, self.y_pos])
        self.y_pos += self.line_height
 
    def reset(self):
        """ Reset text to the top of the screen. """
        self.x_pos = 10
        self.y_pos = 10
        self.line_height = 15
 
    def indent(self):
        """ Indent the next line of text """
        self.x_pos += 10
 
    def unindent(self):
        """ Unindent the next line of text """
        self.x_pos -= 10
 
 
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Initialize the joysticks
pygame.joystick.init()
 
# Get ready to print
textPrint = TextPrint()
 
# -------- Main Program Loop -----------
while not done:
    try:
        # EVENT PROCESSING STEP
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
 
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
            # JOYBUTTONUP JOYHATMOTION
            # if event.type == pygame.JOYBUTTONDOWN:
            #     print("Joystick button pressed.")
            
            # if event.type == pygame.JOYBUTTONUP:
            #     print("Joystick button released.")
 
 
        # DRAWING STEP
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)
        textPrint.reset()
 
        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()
 
        textPrint.pg_print(screen, "Number of joysticks: {}".format(joystick_count))
        textPrint.indent()
 
        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
 
            textPrint.pg_print(screen, "Joystick {}".format(i))
            textPrint.indent()
 
            # Get the name from the OS for the controller/joystick
            name = joystick.get_name()
            textPrint.pg_print(screen, "Joystick name: {}".format(name))
 
            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.pg_print(screen, "Number of axes: {}".format(axes))
            textPrint.indent()
 
            for i in range(axes):
                axis = joystick.get_axis(i)
                textPrint.pg_print(screen, "Axis {} value: {:>6.3f}".format(i, axis))
            textPrint.unindent()
 
            buttons = joystick.get_numbuttons()
            textPrint.pg_print(screen, "Number of buttons: {}".format(buttons))
            textPrint.indent()
 
            for i in range(buttons):
                button = joystick.get_button(i)
                textPrint.pg_print(screen, "Button {:>2} value: {}".format(i, button))
            textPrint.unindent()
 
            # Hat switch. All or nothing for direction, not like joysticks.
            # Value comes back in an array.
            hats = joystick.get_numhats()
            textPrint.pg_print(screen, "Number of hats: {}".format(hats))
            textPrint.indent()
 
            for i in range(hats):
                hat = joystick.get_hat(i)
                textPrint.pg_print(screen, "Hat {} value: {}".format(i, str(hat)))
            textPrint.unindent()
 
            textPrint.unindent()
 
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Update the screen with what we've drawn.
        pygame.display.flip()
 
        # Limit to 60 frames per second
        clock.tick(60)
 
    except (KeyboardInterrupt, SystemExit):
        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE.
        pygame.quit()
        
        # Use the keyboard interrupt from the terminal to break the pygame loop
        done = True