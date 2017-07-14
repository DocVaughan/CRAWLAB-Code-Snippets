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
import planar_crane

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy, GreedyQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory


ENV_NAME = 'planar_crane-v0'

LAYER_SIZE = 2048
NUM_HIDDEN_LAYERS = 4
NUM_STEPS = 2500000
DUEL_DQN = True
TRIAL_ID = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')

# TODO: Add file picker GUI - For now, look for files with the format below
# FILENAME = 'weights/dqn_{}_weights_{}_{}_{}.h5f'.format(ENV_NAME, LAYER_SIZE, NUM_STEPS, TRIAL_ID)
# FILENAME = 'weights/dqn_{}_weights_{}_{}.h5f'.format(ENV_NAME, LAYER_SIZE, NUM_STEPS)
FILENAME = 'weights/duel_dqn_planar_crane-v0_weights_2048_4_2500000_2017-07-12_194502.h5f'

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)

# Record episode data?
env.SAVE_DATA = True

# uncomment to record data about the training session, including video if visualize is true
if DUEL_DQN:
    MONITOR_FILENAME = 'example_data/duel_dqn_{}_monitor_{}_{}_{}_{}'.format(ENV_NAME,
                                                                     LAYER_SIZE,
                                                                     NUM_HIDDEN_LAYERS,
                                                                     NUM_STEPS,
                                                                     TRIAL_ID)
else:
    MONITOR_FILENAME = 'example_data/dqn_{}_monitor_{}_{}_{}_{}'.format(ENV_NAME,
                                                                 LAYER_SIZE,
                                                                 NUM_HIDDEN_LAYERS,
                                                                 NUM_STEPS,
                                                                 TRIAL_ID)
# env = gym.wrappers.Monitor(env, MONITOR_FILENAME, force=True)


# np.random.seed(123)
# env.seed(123)
nb_actions = env.action_space.n


# Next, we build a very simple model.
model = Sequential()

# Input Layer
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))

# Hidden layers
for _ in range(NUM_HIDDEN_LAYERS):
    model.add(Dense(LAYER_SIZE))
    model.add(Activation('relu'))

# Output layer
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())


# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=NUM_STEPS, window_length=1)
# train_policy = BoltzmannQPolicy(tau=0.05)
test_policy = EpsGreedyQPolicy()
train_policy = GreedyQPolicy()

if DUEL_DQN:
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
               enable_dueling_network=True, dueling_type='avg', target_model_update=1e-2, 
               policy=train_policy, test_policy=test_policy)
              
    filename = 'weights/duel_dqn_{}_weights_{}_{}_{}_{}.h5f'.format(ENV_NAME, LAYER_SIZE,  NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)
else:
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
               target_model_update=1e-2, policy=train_policy, test_policy=test_policy)
    
    filename = 'weights/dqn_{}_weights_{}_{}_{}_{}.h5f'.format(ENV_NAME, LAYER_SIZE, NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)


dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Load the model weights
dqn.load_weights(FILENAME)

# Finally, evaluate our algorithm for 1 episode.
dqn.test(env, nb_episodes=5, visualize=True, nb_max_episode_steps=501)