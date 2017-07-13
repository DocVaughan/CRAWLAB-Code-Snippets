#! /usr/bin/env python

###############################################################################
# openAI_planarCrane_train.py
#
# File to train on the CRAWLAB custom OpenAI planar crane environment 
#
# Requires:
#  * CRAWLAB planar_crane Open_AI environment folder to be in the same as this file
#  * keras, openAI gym, keras-rl packages (all are pip or conda installable)
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 07/09/17
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * Add GUI file picker or CLI argument parser for weight filename
###############################################################################

import numpy as np
import datetime     # used to generate unique filenames

import gym
import planar_crane_continuous

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, merge
from keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess


ENV_NAME = 'planar_crane_continuous-v0'

LAYER_SIZE = 2048
NUM_HIDDEN_LAYERS = 3
NUM_STEPS = 50000
TRIAL_ID = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.shape[0]

# Record episode data?
env.SAVE_DATA = False

# uncomment to record data about the training session, including video if visualize is true
MONITOR_FILENAME = 'example_data/ddpg_{}_monitor_{}_{}_{}_{}'.format(ENV_NAME,
                                                                 LAYER_SIZE,
                                                                 NUM_HIDDEN_LAYERS,
                                                                 NUM_STEPS,
                                                                 TRIAL_ID)

env = gym.wrappers.Monitor(env, MONITOR_FILENAME, video_callable=False, force=True)




# Next, we build a very simple actor model.
actor = Sequential()

# Input Layer
actor.add(Flatten(input_shape=(1,) + env.observation_space.shape))

# Hidden layers
for _ in range(NUM_HIDDEN_LAYERS):
    actor.add(Dense(LAYER_SIZE))
    actor.add(Activation('relu'))

# Output layer
actor.add(Dense(nb_actions))
actor.add(Activation('linear'))
print(actor.summary())


# critic model
action_input = Input(shape=(nb_actions,), name='action_input')
observation_input = Input(shape=(1,) + env.observation_space.shape, name='observation_input')
flattened_observation = Flatten()(observation_input)
x = merge([action_input, flattened_observation], mode='concat')

# Hidden layers
for _ in range(NUM_HIDDEN_LAYERS):
    x = (Dense(LAYER_SIZE))(x)
    x = Activation('relu')(x)

# Output Layer
x = Dense(1)(x)
x = Activation('linear')(x)
critic = Model(input=[action_input, observation_input], output=x)
print(critic.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=2*NUM_STEPS, window_length=1)
random_process = OrnsteinUhlenbeckProcess(size=nb_actions, theta=.15, mu=0., sigma=.3)
agent = DDPGAgent(nb_actions=nb_actions, actor=actor, critic=critic, critic_action_input=action_input,
                  memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100,
                  random_process=random_process, gamma=.99, target_model_update=1e-3)
agent.compile(Adam(lr=.001, clipnorm=1.), metrics=['mae'])




# Optionally, we can reload a previous model's weights and continue training from there
# Remove the _actor or _critic from the filename. The load method automatically
# appends these.
# WEIGHTS_FILENAME = 'weights/ddpg_planar_crane_continuous-v0_weights_32_4_50000_2017-07-13_134945.h5f'
# agent.load_weights(WEIGHTS_FILENAME)

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
agent.fit(env, nb_steps=NUM_STEPS, visualize=False, verbose=1, nb_max_episode_steps=500)

# After training is done, we save the final weights.
filename = 'weights/ddpg_{}_weights_{}_{}_{}_{}.h5f'.format(ENV_NAME, LAYER_SIZE, NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)
agent.save_weights(filename, overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
agent.test(env, nb_episodes=5, nb_max_episode_steps=500, visualize=True)
