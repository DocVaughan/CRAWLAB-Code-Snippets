#! /usr/bin/env python

def get_local_extrema(time,data)
    # Get local maximums
    localMax_indexes = signal.argrelextrema(data, np.greater)
    localMaxes = data[localMax_indexes]
    localMax_Times = time[localMax_indexes]

    # Get local minimums
    localMin_indexes = signal.argrelextrema(data, np.less)
    localMins = data[localMin_indexes]
    localMin_Times = time[localMin_indexes]
    
    retrun localMaxes, localMax_Times, localMins, localMin_Times