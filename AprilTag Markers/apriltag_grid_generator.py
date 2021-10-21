#! /usr/bin/env python

###############################################################################
# apriltag_grid_generator.py
#
# Script to generate a calibration grid of AprilTags using the moms-apriltag
# package. Code adapted from that at:
#    https://github.com/MomsFriendlyRobotCompany/moms_apriltag
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 10/21/21
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - @doc_vaughan
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
###############################################################################

import moms_apriltag as apt
import numpy as np
import imageio


if __name__ == '__main__':
    family = "tag36h11"
    shape = (4,6)
    filename = "apriltag_checkerboard_36h11.png"
    size = 50

    target = apt.board(shape, family, size)
    imageio.imwrite(filename, target)