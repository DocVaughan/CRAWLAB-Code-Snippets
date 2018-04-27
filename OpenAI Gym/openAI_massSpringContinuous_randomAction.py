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
import mass_spring_damper_continuous

env = gym.make('mass_spring_damper_continuous-v0')

m1 = 1
m2 = 1

# run 5 episodes of 1000 timesteps, taking random actions at each step
for i_episode in range(5):
    observation = env.reset()
    for t in range(1000):
        env.render()
        
        # just randomly choose an action
        action = env.action_space.sample() 
        observation, reward, done, info = env.step(action)
        
        x1, x1_dot, x2, x2_dot = observation
        
        COM_position = (m1 * x1 + m2 * x2) / 2 
        
        # Finally, print the updated state of the system
        print("\033[2J\033[;H") # Clear the terminal each time
        j = 40  # padding
        d = '.' # what to fill with
        print("x1 (m).:".ljust(j,d), '{:+8.3f}'.format(observation[0]))
        print("x1_dot (m/s):".ljust(j,d), '{:+8.3f}'.format(observation[1]))
        print("x2 (m):".ljust(j,d), '{:+8.3f}'.format(observation[2]))
        print("x2_dot (m/s):".ljust(j,d), '{:+8.3f}'.format(observation[3]))
        print("Force Input (N):".ljust(j,d), '{:+8.3f}'.format(action[0]))
        print("Reward:".ljust(j,d), '{:+8.3f}'.format(reward))

        # if episode finishes before full time range, notify
        if done:
            print("\r\nEpisode finished after {} timesteps".format(t+1))
            time.sleep(1)
            break