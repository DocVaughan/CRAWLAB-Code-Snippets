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

vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP

if clientID != -1:
    print ('Connected to remote API server')

    # enable the synchronous mode on the client:
    vrep.simxSynchronous(clientID, True)

   
    # Get the handles for the objects in the scene we want to interact with. The 
    # names here should match the names in the scene in V-REP
    # Get the handles for the two motors
    motors = ['leftMotor', 'rightMotor']
    motor_handles = [vrep.simxGetObjectHandle(clientID, name, vrep.simx_opmode_blocking)[1] for name in motors]

    # Get the handle for the body
    body_handle = vrep.simxGetObjectHandle(clientID, 'body', vrep.simx_opmode_blocking)[1]
    
    # Get the sensor handle
    sensor_handle = vrep.simxGetObjectHandle(clientID, 'BubbleRobSensingNose', vrep.simx_opmode_blocking)[1]
    
    dt = 0.05 # timestep of the simulation
    vrep.simxSetFloatingParameter(clientID,
                                  vrep.sim_floatparam_simulation_time_step,
                                  dt, # specify a simulation time step
                                  vrep.simx_opmode_oneshot)
 

    # start the simulation sychronized with our code
    vrep.simxStartSimulation(clientID, vrep.simx_opmode_blocking)

    sim_time = 0
    
    try:
        while sim_time < 10: # run for 10 simulated seconds
 
            if sim_time < 7:
                right_motor_speed = 360 * np.pi/180
                left_motor_speed = 360 * np.pi/180
            elif sim_time < 8:
                right_motor_speed = 360 * np.pi/180
                left_motor_speed = -360 * np.pi/180
            

            # Get the position of the boddy at each timestep and print it out, 
            # -1 in this call means absolute position
            _, (x, y, z) = vrep.simxGetObjectPosition(clientID, body_handle, -1, vrep.simx_opmode_blocking)
            print('x: {:5.2f} \t y: {:5.2f} \t z: {:5.2f}'.format(x, y, z))
            
            # Get the sensor data
            _, sensor_status, detected_point, detected_object, dectected_normal_vector = vrep.simxReadProximitySensor(clientID, sensor_handle, vrep.simx_opmode_blocking)

            # If there is something in front of the BubbleRob, then turn
            if sim_time > 0 and detected_point[0] < 0.5:
                right_motor_speed = 720 * np.pi/180
                left_motor_speed = -720 * np.pi/180
                print('Detected object at ({:5.2f}, {:5.2f}, {:5.2f})\r\n'.format(detected_point[0], detected_point[1], detected_point[2]))

            # Set the motor velocities
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
