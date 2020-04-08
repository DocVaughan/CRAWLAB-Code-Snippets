#! /usr/bin/env python

###############################################################################
# tf_agents_randomAgent.py
#
# A simple random agent
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 02/17/20
#   - Joshua Vaughan
#   - vaughanje@ornl.gov or joshua.vaughan@louisiana.edu
#   - @doc_vaughan
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
import logging
import os, sys

import gym


# The world's simplest agent!
class RandomAgent(object):
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()

if __name__ == '__main__':
    # You can optionally set up the logger. Also fine to set the level
    # to logging.DEBUG or logging.WARN if you want to change the
    # amount of output.
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Initilize the environment
    env = gym.make('CartPole-v0')

    # Create the random agent
    agent = RandomAgent(env.action_space)

    episode_count = 100
    max_steps = 200
    reward = 0
    total_reward = 0
    done = False
    
    action_strings = ['None', 'Left', 'Right', 'Down', 'Stop', '???']

    for episode in range(episode_count):
        ob = env.reset()
        total_reward = 0

        for j in range(max_steps):
            env.render()
            action = agent.act(ob, reward, done)
            # The observation is the current game window as an array
            observation, reward, done, _ = env.step(action)
            total_reward = total_reward + reward

            # Finally, print the updated state of the system
            print("\033[2J\033[;H") # Clear the terminal each time
            j = 40  # padding
            d = '.' # what to fill with
            print("Epdisode Number: {:4d}".format(episode))
            print("---------------------")
            print("Current Input".ljust(j,d), '     {:>s}'.format(action_strings[action]))
            print("Current Step Reward".ljust(j,d), '{:>+10.3f}'.format(reward))
            print("Total Episode Reward".ljust(j,d), '{:>+10.3f}'.format(total_reward))

            if done:
                break

    env.close()