#! /usr/bin/env python

###############################################################################
# keras_examine_weights.py
#
# script to examine the weights saved by Keras as .h5f file
#
# Modified from:
#  https://github.com/fchollet/keras/issues/91
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 07/14/17
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

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

import h5py

FILENAME = '../OpenAI Gym/weights/ddpg_planar_crane_continuous-v0_weights_2048_3_100000_2017-07-14_163738_actor.h5f'

def print_structure(weight_file_path):
    """
    Prints out the structure of HDF5 file.

    Args:
      weight_file_path (str) : Path to the file to analyze
    """
    f = h5py.File(weight_file_path)
    try:
        if len(f.attrs.items()):
            print("{} contains: ".format(weight_file_path))
            print("Root attributes:")
        for key, value in f.attrs.items():
            print("  {}: {}".format(key, value))

        if len(f.items())==0:
            return 

        for layer, g in f.items():
            print("  {}".format(layer))
            print("    Attributes:")
            for key, value in g.attrs.items():
                print("      {}: {}".format(key, value))

            print("    Dataset:")
            for p_name in g.keys():
                param = g[p_name]
                print("      {}: {}".format(p_name, param))
    finally:
        f.close()
        
if __name__ == '__main__':
    print_structure(FILENAME)