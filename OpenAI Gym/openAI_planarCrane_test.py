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

from rl.agents.cem import CEMAgent
from rl.agents.dqn import DQNAgent
from rl.agents.sarsa import SarsaAgent
from rl.policy import BoltzmannQPolicy, GreedyQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory, EpisodeParameterMemory


ENV_NAME = 'planar_crane-v0'

LAYER_SIZE = 128
NUM_HIDDEN_LAYERS = 3
NUM_STEPS = 50000
LOG_INTERVAL = 10000
MAX_STEPS = 500
METHOD = 'DUEL_DQN' # can be DQN, DUEL_DQN, SARSA, or CEM
TRIAL_ID = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')

# TODO: 07/14/17 - JEV - Add GUI, argparser, or CLI for this selection
# WEIGHT_FILENAME = 'weights/DUEL_DQN_planar_crane-v0_weights_128_3_250000_2017-07-18_161858.h5f'
WEIGHT_FILENAME = 'weights/{}_{}_weights.h5f'.format(METHOD, ENV_NAME)

# Define the filenames to use for this session
MONITOR_FILENAME = 'example_data/{}_{}_monitor_{}_{}_{}_{}'.format(METHOD, ENV_NAME, LAYER_SIZE, NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)

# Record episode data?
env.SAVE_DATA = True
env.MAX_STEPS = MAX_STEPS

# uncomment to record data about the training session, including video if video_callable is true
# env = gym.wrappers.Monitor(env, MONITOR_FILENAME, video_callable=False, force=True)


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
train_policy = EpsGreedyQPolicy()
test_policy = GreedyQPolicy()


# Compile the agent based on method specified. We use .upper() to convert to 
# upper case for comparison
if METHOD.upper() == 'DUEL_DQN': 
    memory = SequentialMemory(limit=NUM_STEPS, window_length=1)
    agent = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
               enable_dueling_network=True, dueling_type='avg', target_model_update=1e-2, 
               policy=train_policy, test_policy=test_policy)
    agent.compile(Adam(lr=1e-3, clipnorm=1.0), metrics=['mae'])

elif METHOD.upper() == 'DQN':
    memory = SequentialMemory(limit=NUM_STEPS, window_length=1)
    agent = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
               target_model_update=1e-2, policy=train_policy, test_policy=test_policy)
    agent.compile(Adam(lr=1e-3, clipnorm=1.0), metrics=['mae'])

elif METHOD.upper() == 'SARSA':
     # SARSA does not require a memory.
    agent = SarsaAgent(model=model, nb_actions=nb_actions, nb_steps_warmup=10, policy=train_policy)
    agent.compile(Adam(lr=1e-3, clipnorm=1.0), metrics=['mae'])
    
elif METHOD.upper() == 'CEM':
    memory = EpisodeParameterMemory(limit=1000, window_length=1)
    agent = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
               batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
    agent.compile()
    
else:
    raise('Please select  DQN, DUEL_DQN, SARSA, or CEM for your method type.')



# Load the model weights
agent.load_weights(WEIGHT_FILENAME)

# Finally, evaluate our algorithm for 1 episode.
agent.test(env, nb_episodes=5, visualize=True, action_repetition=5)#, nb_max_episode_steps=500)