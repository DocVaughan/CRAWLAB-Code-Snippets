#! /usr/bin/env python

###############################################################################
# mass_spring_damper_continuous.py
#
# Defines a openAI Gym environment for use a two mass-spring-damper system.
# This version has a continuous range of inputs for the m1 force input.
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 04/08/18
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
import datetime # for unique filenames

# Import the ODE solver
from scipy.integrate import odeint

logger = logging.getLogger(__name__)


class MassSpringDamperContEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }
    

    def __init__(self):
        self.m1 = 1.0                   # mass of the mass 1 (kg)
        self.m2 = 1.0                   # mass of the mass 2(kg)
        self.k = 2*np.pi**2             # spring constant (N/m)
        self.spring_equil = 1.0         # equilibrium length of spring 0.25 m
        self.c = 0.0                    # damping coefficient (Ns/m)
        
        self.tau = 0.02                 # seconds between state updates
        self.counter = 0                # counter for number of steps
        self.desired_position = 0       # desired final position of system
        self.max_force = 25.0           # maximum force allowed (N)
        self.SAVE_DATA = False          # set True to save episode data
        self.MAX_STEPS = 500            # maximum number of steps to run
        
        # Define thesholds for trial limits, penalized heavily for exceeding these
        self.mass_pos_threshold = 4.0                 # max mass position (m)
        self.mass_vel_threshold = 0.5                 # max mass velocity (m/s)
        
        # Set up solver parameters
        # ODE solver parameters
        self.abserr = 1.0e-9
        self.relerr = 1.0e-9
        self.max_step = 0.1

        # This action space is the range of acceleration of the trolley
        self.action_space = spaces.Box(low=-self.max_force,
                                       high=self.max_force, 
                                       shape = (1,))
        
        high_limit = np.array([self.mass_pos_threshold,     # max observable angle 
                               self.mass_vel_threshold,     # max observable angular vel.
                               self.mass_pos_threshold,     # max observable position
                               self.mass_vel_threshold])    # max observable cable vel

        low_limit = -high_limit # limits are symmetric about 0
        
        self.observation_space = spaces.Box(high_limit, low_limit)

        self._seed()
        self.viewer = None
        self.state = None
        self.done = False
        self.force = 0.0
        
    def eq_of_motion(self, w, t):
        """
        Defines the differential equations for the coupled spring-mass system.

        Arguments:
            w :  vector of the state variables:
            t :  time
        """
    
        x1 = w[0]
        x1_dot = w[1]
        x2 = w[2]
        x2_dot = w[3]

        # Create sysODE = (x', x_dot', y', y_dot')
        sysODE = np.array([x1_dot,
                           1 / self.m1 * (self.k * (x2 - x1 - self.spring_equil) + self.c * (x2_dot - x1_dot) + self.force),
                           x2_dot,
                           1 / self.m2 * (-self.k * (x2 - x1 - self.spring_equil) + -self.c * (x2_dot - x1_dot))])
    
        return sysODE

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


    def _step(self, action):
        x1, x1_dot, x2, x2_dot = self.state
        self.counter = self.counter + 1
        
        # Get the action and clip it to the min/max trolley accel
        self.force = np.clip(action[0], -self.max_force, self.max_force)
        
        x0 = [x1, x1_dot, x2, x2_dot]

        # Call the ODE solver.
        solution = odeint(self.eq_of_motion, 
                             [0, self.tau], 
                             x0, 
                             max_step=self.max_step, 
                             atol=self.abserr, 
                             rtol=self.relerr)

        resp = solution.y
        
        # Update m1 states
#         x1_accel = 1 / self.m1 * (self.k * (x2 - x1 - self.spring_equil) + 
#                                   self.c * (x2_dot - x1_dot) + 
#                                   self.force)
#         
#         
#         x1_dot = x1_dot + self.tau * x1_accel
#         
#         # Get the action and clip it to the min/max m1 vel
#         x1_dot = np.clip(x1_dot, -self.mass_vel_threshold, self.mass_vel_threshold)
#         
#         x1  = x1 + self.tau * x1_dot
# 
#         # Update m2 states
#         x2_accel = 1 / self.m2 * (-self.k * (x2 - x1 - self.spring_equil) + 
#                                   -self.c * (x2_dot - x1_dot))
#         
#         
#         x2_dot = x2_dot + self.tau * x2_accel
#         
#         # Get the action and clip it to the min/max m2 accel
#         x2_dot = np.clip(x2_dot, -self.mass_vel_threshold, self.mass_vel_threshold)
#        
#         x2  = x2 + self.tau * x2_dot
        
        x1 = resp[0, -1]
        x1_dot = resp[1, -1]
        x2 = resp[2, -1]
        x2_dot = resp[3, -1]

        self.state = (x1, x1_dot, x2, x2_dot)
        
        # Define a boolean on whether we're exceeding limits or not. We'll just penalize
        # any of these conditions identically in the reward function
        limits =  x1 > self.mass_pos_threshold \
               or x1 < -self.mass_pos_threshold \
               or x1_dot > self.mass_vel_threshold \
               or x1_dot < -self.mass_vel_threshold \
               or x2 > self.mass_pos_threshold \
               or x2 < -self.mass_pos_threshold \
               or x2_dot > self.mass_vel_threshold \
               or x2_dot < -self.mass_vel_threshold \


        # TODO: 04/08/18 - This has *huge* effect on the outcome. Decide "optimal" reward scheme.
        # Use COM position
        #distance_to_target = self.desired_position - (self.m1 * x1 + self.m2 * x2) / (self.m1 + self.m2)
        
        # Use m2 position 
        distance_to_target = self.desired_position - x2
        
        # clip the reward to +/-10
        reward = np.clip(-10*distance_to_target**2 - self.force**2, -10, 1)
        
        if self.SAVE_DATA:
            current_data = np.array([self.counter * self.tau, x1, x1_dot, x2, x2_dot, self.force, reward])
            self.episode_data[self.counter, :] = current_data

        if self.counter >= self.MAX_STEPS:
            self.done = True
        
        if self.done == True and self.SAVE_DATA:
            header = header='Time (s), x1 (m), x1_dot (m/s), x2 (m), x2_dot (m/s), Force (N), Reward'
            data_filename = 'example_data/EpisodeData_{}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))
            np.savetxt(data_filename, self.episode_data,  header=header, delimiter=',')

        return np.array(self.state), reward, self.done, {}

    def _reset(self):
        # TODO: 07/07/17 - Probably need more randomness in initial conditions
        rand_pos = self.np_random.uniform(low=-3.0, high=3.0)
        
        self.state = np.array([rand_pos, 
                               0, 
                               rand_pos + self.spring_equil,
                               0])

        # Reset the counter and the data recorder array
        self.counter = 0
        
        # Reset the done flag
        self.done = False

        if self.SAVE_DATA:
            self.episode_data = np.zeros((self.MAX_STEPS+1, 7))
            self.episode_data[0,:] = np.array([0, self.state[0], self.state[1], self.state[2], self.state[3], 0, 0])

        return np.array(self.state)

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        screen_width = 600
        screen_height = 400

        world_width = 1.5 * self.mass_pos_threshold
        scale = screen_width / world_width        # Scale according to width
        
        
        # Define the mass size and its offset from the bottom of the screen (pixels)
        mass_width = 30.0 
        mass_height = 30.0
        mass_yOffset = screen_height/2
        
        target_size = 10
        COM_size = 5

        x1, x1_dot, x2, x2_dot = self.state
        
        COM_position = (self.m1 * x1 + self.m2 * (x2)) / (self.m1 + self.m2)

        if self.viewer is None: # Initial scene setup
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            
            # the target is a series of circles, a bullseye
            self.target = rendering.make_circle(target_size*2)
            self.targettrans = rendering.Transform(translation=(screen_width/2 + self.desired_position*scale, mass_yOffset))
            self.target.add_attr(self.targettrans)
            self.target.set_color(1,0,0)  # red
            self.viewer.add_geom(self.target)
            
            self.target = rendering.make_circle(target_size*1.25)
            self.targettrans = rendering.Transform(translation=(screen_width/2 + self.desired_position*scale, mass_yOffset))
            self.target.add_attr(self.targettrans)
            self.target.set_color(1,1,1)  # white
            self.viewer.add_geom(self.target)
            
            self.target = rendering.make_circle(target_size/2)
            self.targettrans = rendering.Transform(translation=(screen_width/2 + self.desired_position*scale, mass_yOffset))
            self.target.add_attr(self.targettrans)
            self.target.set_color(1,0,0)  # red
            self.viewer.add_geom(self.target)
            
            
            # the COM is a series of circles, a bullseye
            self.COM1 = rendering.make_circle(COM_size*2)
            self.COM1trans = rendering.Transform(translation=(screen_width/2 + COM_position*scale, mass_yOffset))
            self.COM1.add_attr(self.COM1trans)
            self.COM1.set_color(0,0,0)  # black
            self.viewer.add_geom(self.COM1)
            
            self.COM2 = rendering.make_circle(COM_size*1.25)
            self.COM2trans = rendering.Transform(translation=(screen_width/2 + COM_position*scale, mass_yOffset))
            self.COM2.add_attr(self.COM2trans)
            self.COM2.set_color(1,1,1)  # white
            self.viewer.add_geom(self.COM2)
            
            self.COM3 = rendering.make_circle(COM_size/2)
            self.COM3trans = rendering.Transform(translation=(screen_width/2 + COM_position*scale, mass_yOffset))
            self.COM3.add_attr(self.COM3trans)
            self.COM3.set_color(0,0,0)  # black
            self.viewer.add_geom(self.COM3)
            
            
            # Define the trolley polygon
            l,r,t,b = -mass_width/2, mass_width/2, mass_height/2, -mass_height/2
            
            self.mass1 = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            self.mass1trans = rendering.Transform(translation=(screen_width/2 + x1*scale, mass_yOffset))
            self.mass1.add_attr(self.mass1trans)
            self.mass1.set_color(0.85,0.85,0.85)    # light gray
            self.viewer.add_geom(self.mass1)
            
            self.mass2 = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            self.mass2trans = rendering.Transform(translation=(screen_width/2 + x2*scale, mass_yOffset))
            self.mass2.add_attr(self.mass2trans)
            self.mass2.set_color(0.85,0.85,0.85)    # light gray
            self.viewer.add_geom(self.mass2)
            
            
            # This is a bar that shows the direction of the current accel. command
            l,r,t,b = -10.0, 10.0, 4, -4
            self.accel = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            self.acceltrans = rendering.Transform(translation=(screen_width/2 + x1*scale-mass_width/2, mass_yOffset))
            self.accel.add_attr(self.acceltrans)
            self.accel.set_color(0.1, 0.1, 0.5)
            self.viewer.add_geom(self.accel)

        
        # move the trolley
        self.mass1trans.set_translation(screen_width/2 + x1*scale, mass_yOffset)
        self.mass2trans.set_translation(screen_width/2 + x2*scale, mass_yOffset)
        self.COM1trans.set_translation(screen_width/2 + COM_position*scale, mass_yOffset)
        self.COM2trans.set_translation(screen_width/2 + COM_position*scale, mass_yOffset)
        self.COM3trans.set_translation(screen_width/2 + COM_position*scale, mass_yOffset)
        
        # show the accel direction
        accel_scaling = 1 / (25 * self.max_force) * self.force * scale
        self.acceltrans.set_translation(screen_width/2 + (x1*scale + (accel_scaling/2)), mass_yOffset)
        self.acceltrans.set_scale(accel_scaling, 1)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')