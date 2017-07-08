#! /usr/bin/env python

###############################################################################
# openAI_variableLengthPendulum.py
#
# script to run the variable lenght pendulum OpenAI environment
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 07/07/17
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

import gym
import time
import variable_pendulum

env = gym.make('variable_pendulum-v0')

# run 5 episodes of 1000 timesteps, taking random actions at each step
for i_episode in range(5):
    observation = env.reset()
    for t in range(1000):
        env.render()
        
        # just randomly choose an action
        action = env.action_space.sample() 
        observation, reward, done, info = env.step(action)
        
        # Finally, print the updated state of the system
        print("\033[2J\033[;H") # Clear the terminal each time
        j = 40  # padding
        d = '.' # what to fill with
        print("Theta (deg).:".ljust(j,d), '{:+8.3f}'.format(observation[0]*180/np.pi))
        print("Theta_dot (deg/s).:".ljust(j,d), '{:+8.3f}'.format(observation[1]*180/np.pi))
        print("L (m).:".ljust(j,d), '{:+8.3f}'.format(observation[2]))
        print("L_dot (m/s).:".ljust(j,d), '{:+8.3f}'.format(observation[3]))
        print("Reward:".ljust(j,d), '{:+8.3f}'.format(reward))

        # if episode finishes before full time range, notify
        if done:
            print("\r\nEpisode finished after {} timesteps".format(t+1))
            time.sleep(1)
            break