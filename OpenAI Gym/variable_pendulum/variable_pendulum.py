#! /usr/bin/env python

###############################################################################
# variable_pendulum.py
#
# Defines a variable-length pendulum environment for use with the openAI Gym.
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


class VariablePendulumEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }
    
    # actions available, hoist down, do nothing, hoist up
    MAX_CABLE_ACCEL = 2.0
    AVAIL_CABLE_ACCEL =  [-MAX_CABLE_ACCEL, 0, MAX_CABLE_ACCEL]  

    def __init__(self):
        self.gravity = 9.8          # accel. due to gravity (m/s^2)
        self.masspend = 1.0         # mass of the pendulum point mass (kg)
        self.max_cable_accel = 0.25 # maximum acceleration of cable (m/s^2)
        self.counter = 0            # counter to trial duration
        self.tau = 0.02             # seconds between state updates

        
        # Define thesholds for limit penalty
        self.l_max_threshold = 3.5                  # max cable length (m)
        self.l_min_threshold = 0.5                  # min cable length (m)
        self.l_dot_threshold = 0.5                  # max cable speed (m/s)
        self.theta_mag_threshold = 45*np.pi/180     # max angle amplitude

        # This action space is just hoist down, do nothing, hoist up
        self.action_space = spaces.Discrete(3)
        
#         high_limit = np.array([2*self.theta_threshold, # max observable angle 
#                                10*2*self.theta_threshold, # max observable angular vel.
#                                10,                     # max observable length
#                                2])                     # max observable cable vel
#         
#         low_limit = np.array([-2*self.theta_threshold, # max observable angle 
#                               -10*2*self.theta_threshold, # max observable angular vel.
#                               0,                     # max observable length
#                               -2])                     # max observable cable vel

        high_limit = np.array([1.0, # max observable cos(angle) 
                               1.0, # max observable sin(angle) 
                               1.2 * np.sqrt(self.gravity/self.l_min_threshold),
                               4,                     # max observable length
                               2])                     # max observable cable vel
        
        low_limit = np.array([-1.0, # min observable cos(angle)
                              -1.0, # max observable sin(angle)
                              -1.2*np.sqrt(self.gravity/self.l_min_threshold),
                              0,                     # max observable length
                              -2])                     # max observable cable vel
        
                             
        self.observation_space = spaces.Box(high_limit, low_limit)

        self._seed()
        self.viewer = None
        self.state = None
        self.cable_accel = 0
        self.l_init = None

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        theta, theta_dot, l, l_dot = self.state
        self.cable_accel = self.AVAIL_CABLE_ACCEL[action]
        
        # We can enforce limits on the cable length
#         if l >= self.l_max_threshold and self.cable_accel > 0:
#             self.cable_accel = 0
#         elif l<=self.l_min_threshold and self.cable_accel < 0:
#             self.cable_accel = 0
                
        theta_ddot = -l_dot/l * theta_dot - self.gravity/l * np.sin(theta)
        l_ddot = self.cable_accel

        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * theta_ddot

        l  = l + self.tau * l_dot
        l_dot = l_dot + self.tau * l_ddot
        
        # Uncomment below to clip l and theta- the physics in the sim won't be right.
        #l = np.clip(l, self.l_min_threshold, self.l_max_threshold)
        #theta = np.clip(theta, -self.theta_threshold, self.theta_threshold)
        
        self.state = (theta, theta_dot, l, l_dot)
        
        limits =  l > self.l_max_threshold \
                  or l < self.l_min_threshold \
                  or l_dot > self.l_dot_threshold \
                  or l_dot < -self.l_dot_threshold\
                  or theta > self.theta_mag_threshold \
                  or theta < -self.theta_mag_threshold


        # TODO: 07/09/17 - This has *huge* effect on the outcome. Decide "optimal" reward scheme.
        distance_from_target_squared = (self.l_init - l * np.cos(theta))**2 + (l * np.sin(theta))**2
        #reward = -1.0 + 0.001 / (distance_to_target)**2 - 0.0001*self.x_accel**2 - limits*10
            
        if distance_from_target_squared >= 0.001: #or np.abs(l_dot) > np.pi/180:
#             reward = -1.0 - 10*theta**2 - 0.1*self.cable_accel**2 - limits*10
            reward = -1.0 - 100*distance_from_target_squared - 0.01*self.cable_accel**2 - limits*10
        else:  
            reward = 10000.0
        
        if self.counter > 500:
            done = True
        else:
            done = False

        return self._get_obs(), reward, done, {}
        
    def _get_obs(self):
        theta, theta_dot, l, l_dot = self.state
        
        # For this environment we return the cosine and sine of the angle
        # rather than returning the angle directly
        return np.array([np.cos(theta), np.sin(theta), theta_dot, l, l_dot])

    def _reset(self):
#         self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        # TODO: 07/07/17 - Probably need more randomness in initial conditions
        self.state = np.array([self.np_random.uniform(low=-2*np.pi/180, high=2*np.pi/180),
                               self.np_random.uniform(low=-np.pi/6, high=np.pi/6),
                               2,#self.np_random.uniform(low=1.5*self.l_min_threshold, high=0.5*self.l_max_threshold),
                               0])#self.np_random.uniform(low=-0.5, high=0.5)])
        self.l_init = self.state[2]
        self.counter = 0
        return self._get_obs()

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        screen_width = 600
        screen_height = 400

        world_width = 2 * self.l_max_threshold# * np.sin(self.theta_threshold)
        world_height = 1.5 * self.l_max_threshold
#         scale = screen_width/world_width  # Scale according to width
        scale = screen_height/world_height    # Scale according to height
        cable_pin = screen_height - 10
        payload_size = 10.0
        cable_width = 2.0
        

        theta, theta_dot, l, l_dot = self.state

        if self.viewer is None:
            self.l_init_view = l # save the initial length for scaling cable
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            
            # define the cable as a polygon, so we can change its length later
            lf,r,t,b = -cable_width/2, cable_width/2, cable_width/2, -l*scale-cable_width/2
            self.cable = rendering.FilledPolygon([(lf,b), (lf,t), (r,t), (r,b)])
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
            
            self.hoist = rendering.FilledPolygon([(lf,b), (lf,t), (r,t), (r,b)])
            self.hoisttrans = rendering.Transform(translation=(screen_width - 10, screen_height/2))
            self.hoist.add_attr(self.hoisttrans)
            self.hoist.set_color(0.5,0.6,0.75)
            self.viewer.add_geom(self.hoist)

        # calculate the payload position in the window, then move it there
        payload_screen_x = screen_width/2 + l*np.sin(theta)*scale
        payload_screen_y = cable_pin - l*np.cos(theta)*scale
        self.payloadtrans.set_translation(payload_screen_x, payload_screen_y)

        # rotate the cable
        self.cabletrans.set_rotation(theta)
        
        # change its length by scaling its length relative to its initial length
        self.cabletrans.set_scale(1, l/self.l_init_view)
        
        # change the scaling of the hoist indicator to indicate hoist action
        self.hoisttrans.set_scale(1, np.sign(self.cable_accel))

        return self.viewer.render(return_rgb_array = mode=='rgb_array')