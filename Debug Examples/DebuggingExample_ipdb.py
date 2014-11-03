#! /usr/bin/env python

##########################################################################################
# DebuggingExample_ipdb.py
#
# Example demonstrating basic use of ipdb for debugging
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 11/03/14
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

import numpy as np
from matplotlib.pyplot import *

def remove_odd_numbers(array_of_numbers):
    """
    Function to remove the odd numbers from an array_of_numbers
    
    Inputs:
        array_of_numbers : a numpy array
    
    Returns:
        array_of_evens : a numpy array containing the even numbers of array_of_numbers
    """
    
#     import pdb
#     pdb.set_trace()
    
    list_of_numbers = array_of_numbers.tolist()
    
    # print list_of_numbers
    
    # test = list_of_numbers ** 2
    
    
    for number in list_of_numbers:
        if number % 2 == 1:
           list_of_numbers.remove(number)

    return list_of_numbers

def remove_odd_numbers_tolist(array_of_numbers):
    """
    Function to remove the odd numbers from an array_of_numbers
    
    Inputs:
        array_of_numbers : a numpy array
    
    Returns:
        array_of_evens : a numpy array containing the even numbers of array_of_numbers
    """
    
    #import pdb
    #pdb.set_trace()
    
    # Define an empty array for evens
    array_of_evens = []
    
    # Note: iterating over large lists is often *slow*
    for number in array_of_numbers.tolist():
        if number % 2 == 0:
           array_of_evens = np.append(array_of_evens, number)
           
    return array_of_evens


def remove_odd_numbers_nditer(array_of_numbers):
    """
    Function to remove the odd numbers from an array_of_numbers
    
    Inputs:
        array_of_numbers : a numpy array
    
    Returns:
        array_of_evens : a numpy array containing the even numbers of array_of_numbers
    """
    
    # Uncomment below to enable line-by-line debugging
    #import pdb
    #pdb.set_trace()
    
    # Define an empty array for evens
    array_of_evens = []
    
    # Note: Using nditer is faster for large lists?
    for number in np.nditer(array_of_numbers):
        if number % 2 == 0:
           array_of_evens = np.append(array_of_evens, number)

    return array_of_evens



if __name__ == "__main__":
    # our_numbers = np.array([0, 1, 2, 3, 4, 5, 6])
    
    our_numbers = np.array([0, 3, 1, 4, 2, 5, 6])
    
    print remove_odd_numbers(our_numbers)
#     print remove_odd_numbers_tolist(our_numbers)
#     print remove_odd_numbers_nditer(our_numbers)
