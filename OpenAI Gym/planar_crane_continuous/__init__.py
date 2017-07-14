#! /usr/bin/env python

###############################################################################
# __init__.py
#
# initialization for the planar_crane_continuous OpenAI environment
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 07/13/17
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

from gym.envs.registration import register

register(
    id='planar_crane_continuous-v0',
    entry_point='planar_crane_continuous.planar_crane_continuous:PlanarCraneContEnv',
)