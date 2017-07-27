#! /usr/bin/env python

###############################################################################
# bubbleRob_example.py
#
# File to drive around the BubbleRob model within V-REP. Load the BubbleRob_example.ttt 
# scene V-REP prior to running this script. 
#
# Also make sure to change the simulation timestep to custom. The pulldown to do
# so is next to the "play" button in V-REP.
#
# Note: This code was extended from simpleSynchronousTest.py provided as a tutorial by V-REP.
# That file was automatically created for V-REP release V3.4.0 rev. 1 on April 5th 2017
#
# Addition help from:
#  https://studywolf.wordpress.com/2016/04/18/using-vrep-for-simulation-of-force-controlled-models/
#
# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19997)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 07/27/17
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

import numpy as np
import matplotlib.pyplot as plt
#
try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time

print ('Program started')

vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP


if clientID!=-1:
    print ('Connected to remote API server')

    # enable the synchronous mode on the client:
    vrep.simxSynchronous(clientID, True)

    motors = ['leftMotor', 'rightMotor']
    
    motor_speeds = np.ones(len(motors)) * 10.0
    
    # get the handles for each joint and set up streaming
    motor_handles = [vrep.simxGetObjectHandle(clientID, name, vrep.simx_opmode_blocking)[1] for name in motors]

    # get handle for target and set up streaming
    _, target_handle = vrep.simxGetObjectHandle(clientID, 'target', vrep.simx_opmode_blocking)

    dt = 0.05 # timestep of the simluation
    vrep.simxSetFloatingParameter(clientID,
                                  vrep.sim_floatparam_simulation_time_step,
                                  dt, # specify a simulation time step
                                  vrep.simx_opmode_oneshot)
 

    # start the simulation in lockstep with our code
    vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)

    sim_time = 0
    try:
        while sim_time < 10: # run for 10 simulated seconds
 
            if sim_time < 2:
                right_motor_speed = 180 * np.pi/180
                left_motor_speed = 180 * np.pi/180
            elif sim_time < 5:
                right_motor_speed = 180 * np.pi/180
                left_motor_speed = -180 * np.pi/180
            else:
                right_motor_speed = -180 * np.pi/180
                left_motor_speed = -180 * np.pi/180
            
            vrep.simxSetJointTargetVelocity(clientID, motor_handles[0], left_motor_speed, vrep.simx_opmode_blocking)
            vrep.simxSetJointTargetVelocity(clientID, motor_handles[1], right_motor_speed, vrep.simx_opmode_blocking)
        
            # move simulation ahead one time step
            vrep.simxSynchronousTrigger(clientID)
            sim_time += dt

    except (KeyboardInterrupt, SystemExit):    
        # stop the simulation:
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)
        
        # Before closing the connection to V-REP,
        #make sure that the last command sent out had time to arrive.
        vrep.simxGetPingTime(clientID)

        # Now close the connection to V-REP:
        vrep.simxFinish(clientID)
        
    finally:
        # stop the simulation:
        vrep.simxStopSimulation(clientID, vrep.simx_opmode_blocking)
        
        # Before closing the connection to V-REP,
        #make sure that the last command sent out had time to arrive.
        vrep.simxGetPingTime(clientID)

        # Now close the connection to V-REP:
        vrep.simxFinish(clientID)
        
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
