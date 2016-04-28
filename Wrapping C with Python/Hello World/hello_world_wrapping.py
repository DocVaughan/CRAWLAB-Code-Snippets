#! /usr/bin/env python

###############################################################################
# hello_world_wrapping.py
#
# Python code to wrap a very simple shared library
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/27/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

# Import the ctypes module. Importing all for now.
from ctypes import *

# Load the libhello_world c code, built as a shared-library
# Give it a name to make it callable
hello = CDLL('libhello_world.dylib')

# Call the int_multiple function from the libhello_world library
result = hello.int_multiply(2, 3)

print('The result is {}.'.format(result))


# Call the hello_world function from the libhello_world library
hello.hello_world()