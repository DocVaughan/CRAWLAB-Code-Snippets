#! /usr/bin/env python

##########################################################################################
# parse_basicData.py
#
# Script to write and read basic data from a parse.com account
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 03/18/15
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import numpy as np
import matplotlib.pyplot as plt
import datetime

from parse_rest.connection import register
from parse_rest.datatypes import Object


class TestData(Object):
    pass
    

if __name__ == '__main__':
    register('mROIEsIqVeYLTXOgrcAODzdWMDiuzmQq6amBecNE', '0mvacQYGeG6136k1xKgMnUSjssdvjnaPge6pfTfE', master_key = 'ZrIxVKXJ5Wo60PIKLpsnzt4y9MJlSJy9DLKarOWX')

    currentTime = datetime.datetime.now().isoformat(' ')
    number_squeezed = 6
    testData = TestData(Time = currentTime, Location = "UL Lafayette", NumberOfTubes = number_squeezed)
    testData.save()
    
    # Read the data
    all_data = TestData.Query.all()

    for data in all_data:
       print data.Time, data.Location, data.NumberOfTubes
    