#! /usr/bin/env python

###############################################################################
# openAI_planarCrane_test.py
#
# File to test on the CRAWLAB custom OpenAI planar crane environment 
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
#   * 
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

# TODO: Add file picker GUI - For now, look for files with the format below
# Remove the _actor or _critic from the filename. The load method automatically
# appends these.
FILENAME = 'weights/ddpg_planar_crane_continuous-v0_weights_2048_3_50000_2017-07-13_200743.h5f'

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
nb_actions = env.action_space.shape[0]

# Record episode data?
env.SAVE_DATA = True
env.MAX_STEPS = 500



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

# Load the model weights - this method will automatically load the weights for
# both the actor and critic
agent.load_weights(FILENAME)


# Finally, evaluate our algorithm for 5 episodes.
agent.test(env, nb_episodes=5, nb_max_episode_steps=500, visualize=True)