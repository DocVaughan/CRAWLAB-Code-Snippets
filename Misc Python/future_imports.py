#! /usr/bin/env python

###############################################################################
# future_imports.py
#
# Testing from future imports
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/25/16
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
###############################################################################

# These two includes will handle most of our cases
from __future__ import division
from __future__ import print_function

# These two may be needed in special cases
# from __future__ import absolute_import
# from __future__ import unicode_literals

# Our "normal" imports
import numpy as np
import matplotlib.pyplot as plt
import sys # Needed to get the python version

print('Hello')

print('Hello from a print function in Python {}!'.format(sys.version[0:3]))

print('1/3 = {}'.format(1/3))