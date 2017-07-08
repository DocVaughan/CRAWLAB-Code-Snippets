#! /usr/bin/env python

###############################################################################
# variable_pendulum_continuous.py
#
# Defines a variable-length pendulum environment for use with the openAI Gym.
# This version has a continuous range of inputs for the cable length accel.
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


import gym
from gym import spaces
from gym.utils import seeding
import logging
import numpy as np

logger = logging.getLogger(__name__)


class VariablePendulumContEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }
    
    def __init__(self):
        self.gravity = 9.8          # accel. due to gravity (m/s^2)
        self.masspend = 1.0         # mass of the pendulum point mass (kg)
        self.max_cable_accel = 0.25 # maximum acceleration of cable (m/s^2)
        self.tau = 0.02             # seconds between state updates
        self.counter = 0            # counter to limit number of calls

        
        # Define thesholds for failing episode
        self.theta_threshold = 45 * np.pi / 180     # +/- 45 degree limit (rad)
        self.l_max_threshold = 3.0                  # max cable length (m)
        self.l_min_threshold = 0.5                  # min cable length (m)

        # This action space is just hoist down, do nothing, hoist up
        self.action_space = spaces.Box(low=-self.max_cable_accel,
                                       high=self.max_cable_accel, 
                                       shape = (1,))
        
        high_limit = np.array([2*self.theta_threshold, # max observable angle 
                               10*2*self.theta_threshold, # max observable angular vel.
                               5,                     # max observable length
                               2])                     # max observable cable vel
        
        low_limit = np.array([-2*self.theta_threshold, # max observable angle 
                              -10*2*self.theta_threshold, # max observable angular vel.
                              0,                     # max observable length
                              -2])                     # max observable cable vel
                             
        self.observation_space = spaces.Box(high_limit, low_limit)

        self._seed()
        self.viewer = None
        self.state = None

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        self.counter = self.counter + 1
        theta, theta_dot, l, l_dot = self.state

        cable_accel = np.clip(action, -self.max_cable_accel, self.max_cable_accel)[0]
        
        theta_ddot = -l_dot/l * theta_dot - self.gravity/l * np.sin(theta)
        l_ddot = cable_accel

        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * theta_ddot

        l  = l + self.tau * l_dot
        l_dot = l_dot + self.tau * l_ddot
        self.state = (theta, theta_dot, l, l_dot)
        
        done =  l > self.l_max_threshold \
                or l < self.l_min_threshold \
                or theta < -self.theta_threshold \
                or theta > self.theta_threshold \
                or self.counter > 500 \
                or (np.abs(theta) < np.pi/180 and np.abs(theta_dot) < np.pi/180)
        
        done = bool(done)

        if not done:
            reward = 1000.0 / (theta * 180/np.pi)**2
            
            if (np.abs(theta) < np.pi/180):
                reward = reward * 1.2
            
                if (np.abs(theta_dot) < np.pi/180):
                    reward = reward * 1.2
                
        else:
            reward = 0.0

        return np.array(self.state), reward, done, {}

    def _reset(self):
#         self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        # TODO: 07/07/17 - Probably need more randomness in initial conditions
        self.state = np.array([self.np_random.uniform(low=-np.pi/12, high=np.pi/12),
                               0, #self.np_random.uniform(low=-0.5*np.pi/6, high=0.5*np.pi/6),
                               self.np_random.uniform(low=1.5*self.l_min_threshold, high=0.5*self.l_max_threshold),
                               0])#self.np_random.uniform(low=-0.5, high=0.5)])
        self.counter = 0
        return np.array(self.state)

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        screen_width = 600
        screen_height = 400

        world_width = 2 * self.l_max_threshold# * np.sin(self.theta_threshold)
        scale = screen_width/world_width
        cable_pin = screen_height - 10
        payload_size = 10.0
        cable_width = 2.0
        

        theta, theta_dot, l, l_dot = self.state

        if self.viewer is None:
            self.l_init = l # save the initial length for scaling cable
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            
            # define the cable as a polygon, so we can change its length later
            l,r,t,b = -cable_width/2, cable_width/2, cable_width/2, -l*scale-cable_width/2
            self.cable = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            self.cabletrans = rendering.Transform(translation=(screen_width/2, cable_pin))
            self.cable.add_attr(self.cabletrans)
            self.cable.set_color(0.25,0.25,0.25)    # dark gray
            self.viewer.add_geom(self.cable)
            
            # the payload is a circle.
            self.payload = rendering.make_circle(payload_size)
            self.payloadtrans = rendering.Transform(translation=(screen_width/2, cable_pin-l*scale))
            self.payload.add_attr(self.payloadtrans)
            self.payload.set_color(0.5,0.5,0.5)  # mid gray
            self.viewer.add_geom(self.payload)


        if self.state is None: 
            return None

        # calculate the payload position in the window, then move it there
        payload_screen_x = screen_width/2 + l*np.sin(theta)*scale
        payload_screen_y = cable_pin - l*np.cos(theta)*scale
        self.payloadtrans.set_translation(payload_screen_x, payload_screen_y)

        # rotate the cable
        self.cabletrans.set_rotation(theta)
        
        # change its length by scaling its length relative to its initial length
        self.cabletrans.set_scale(1, l/self.l_init)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')