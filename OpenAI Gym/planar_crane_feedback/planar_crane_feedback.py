#! /usr/bin/env python

###############################################################################
# planar_crane.py
#
# Defines a planar crane environment for use with the openAI Gym.
# This version has a continuous range of inputs for the trolley accel. input
# We are treating the trolley in a way that assumes we can exactly control its 
# motion. We specify its acceleration as the input.
# Cable length is constant.
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


class PlanarCraneEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }
    
    # actions available are accel left, do nothing, accel right
    MAX_TROLLEY_ACCEL = 1.0
    AVAIL_TROLLEY_ACCEL =  [-MAX_TROLLEY_ACCEL, 0, MAX_TROLLEY_ACCEL]  
    
    def __init__(self):
        self.gravity = 9.8          # accel. due to gravity (m/s^2)
        self.masspend = 1.0         # mass of the pendulum point mass (kg)
        self.cable_length = 2       # cable length (m)
        self.tau = 0.02             # seconds between state updates
        self.counter = 0            # running counter
        self.time = 0.0             # running time
        
        # Define thesholds for failing episode
        self.theta_threshold = 60 * np.pi / 180     # +/- 45 degree limit (rad)
        self.x_max_threshold = 2.5                  # max trolley position (m)
        self.v_max_threshold = 0.5                  # max trolley velocity (m/s)

        # This action space is just hoist down, do nothing, hoist up
        # self.action_space = spaces.Box(low=-self.max_cable_accel,
#                                        high=self.max_cable_accel, 
#                                        shape = (1,))

        # This action space is just accel left, do nothing, accel right
        self.action_space = spaces.Discrete(3)
        
        high_limit = np.array([2*self.theta_threshold,      # max observable angle 
                               10*2*self.theta_threshold,   # max observable angular vel.
                               self.x_max_threshold,        # max observable position
                               self.v_max_threshold])       # max observable cable vel
        
        low_limit = -high_limit # Limits are symmetric about 0
                             
        self.observation_space = spaces.Box(high_limit, low_limit)

        self._seed()
        self.viewer = None
        self.state = None
        self.x_accel = 0.0

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        theta, theta_dot, x, x_dot = self.state
        self.time = self.time + self.tau
        
        # Update the trolley states
        if self.time > 1.0:
            self.x_accel = self.AVAIL_TROLLEY_ACCEL[action]
        else:
            self.x_accel = 0.0
        x  = x + self.tau * x_dot
        x_dot = x_dot + self.tau * self.x_accel       
        
        # Update the pendulum states
        theta_ddot = -self.gravity / self.cable_length * theta + 1.0 / self.cable_length * self.x_accel
        theta_dot = theta_dot + self.tau * theta_ddot
        theta = theta + self.tau * theta_dot

        self.state = (theta, theta_dot, x, x_dot)
        
        # Define a boolean on whether we're exceeding limits or not. We'll just penalize
        # any of these conditions identically in the reward function
        limits =  x > self.x_max_threshold \
                or x < 0 \
                or theta < -self.theta_threshold \
                or theta > self.theta_threshold \
                or x_dot > self.v_max_threshold \
                or x_dot < -self.v_max_threshold \

        # Just penalize theta
        #reward = -10*theta**2 - theta_dot**2 - 100*limits
        
        distance_to_target = - self.cable_length * np.sin(theta)
        #distance_to_target = self.desired_trolley - x
#         reward = 1 / distance_to_target**2 - 0.01*theta**2#- 0.1 * self.counter*self.tau
            
#         if np.abs(distance_to_target) >= 0.05:
#             reward = -1.0 - 10*theta**2 - 0.1*x_dot**2 - limits*10 #- x**2
#         else:  
#             reward = 1000.0
        
#         reward = -theta**2 - limits*10 #- x**2
        
#         if theta < np.pi/180:
#             reward = 1.0
#             if theta_dot < np.sqrt(self.gravity/self.cable_length) * np.pi/180:
#                 reward = reward * 10
        if np.abs(theta) < 1*np.pi/180:
            reward = 1e3
        else:
            reward = - 1000*theta**2 - theta_dot **2 - 0.1*x_dot**2 - 0.01*self.x_accel**2 - limits*1000 #- x**2
        
        
        return np.array(self.state), reward, False, {}

    def _reset(self):
#         self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        # TODO: 07/07/17 - Probably need more randomness in initial conditions
        self.state = np.array([self.np_random.uniform(low=-np.pi/12, high=np.pi/12),
                               self.np_random.uniform(low=-0.5*np.pi/6, high=0.5*np.pi/6),
                               0,
                               0])#self.np_random.uniform(low=-0.5, high=0.5)])
        return np.array(self.state)

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        screen_width = 600
        screen_height = 400

        world_width = 1.5 * self.x_max_threshold
        scale = screen_width/world_width
        scale = screen_width/world_width  # Scale according to width
        # scale = screen_height/world_height    # Scale according to height
        payload_size = 10.0
        cable_width = 2.0
        
        trolley_width = 50.0
        trolley_height = 30.0
        trolley_yOffset = screen_height-25
        

        theta, theta_dot, x, x_dot = self.state

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            
            # Define the trolley polygon
            l,r,t,b = -trolley_width/2, trolley_width/2, trolley_height/2, -trolley_height/2
            self.trolley = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            self.trolleytrans = rendering.Transform(translation=(screen_width/2 + x*scale, trolley_yOffset))
            self.trolley.add_attr(self.trolleytrans)
            self.trolley.set_color(0.85,0.85,0.85)    # light gray
            self.viewer.add_geom(self.trolley)
            
            # define the cable as a polygon, so we can change its length later
            l,r,t,b = -cable_width/2, cable_width/2, cable_width/2, -self.cable_length*scale-cable_width/2
            self.cable = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            self.cabletrans = rendering.Transform(translation=(screen_width/2 + x*scale, trolley_yOffset))
            self.cable.add_attr(self.cabletrans)
            self.cable.set_color(0.25,0.25,0.25)    # dark gray
            self.viewer.add_geom(self.cable)
            
            # the payload is a circle.
            self.payload = rendering.make_circle(payload_size)
            self.payloadtrans = rendering.Transform(translation=(screen_width/2 + x*scale, trolley_yOffset-self.cable_length))
            self.payload.add_attr(self.payloadtrans)
            self.payload.set_color(0.5,0.5,0.5)  # mid gray
            self.viewer.add_geom(self.payload)
            
            l,r,t,b = -10.0, 10.0, cable_width/2, -cable_width/2
            self.accel = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            self.acceltrans = rendering.Transform(translation=(screen_width/2 + x*scale-trolley_width/2, trolley_yOffset))
            self.accel.add_attr(self.acceltrans)
            self.accel.set_color(0.1, 0.1, 0.5)
            self.viewer.add_geom(self.accel)
            
        if self.state is None: 
            return None

        # calculate the payload position in the window, then move it there
        payload_screen_x = (x - self.cable_length*np.sin(theta))*scale
        payload_screen_y = trolley_yOffset - self.cable_length*np.cos(theta)*scale
        self.payloadtrans.set_translation(screen_width/2 + payload_screen_x, payload_screen_y)

        # rotate the cable
        self.cabletrans.set_translation(screen_width/2 + x*scale, trolley_yOffset)
        self.cabletrans.set_rotation(-theta)
        
        # move the trolley
        self.trolleytrans.set_translation(screen_width/2 + x*scale, trolley_yOffset)
        
        # show the accel direction
        self.acceltrans.set_translation(screen_width/2 + (x*scale + np.sign(self.x_accel)*(trolley_width/2+10)), trolley_yOffset)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')