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
import planar_crane

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam


from rl.agents.cem import CEMAgent
from rl.agents.dqn import DQNAgent
from rl.agents.sarsa import SarsaAgent
from rl.policy import BoltzmannQPolicy, GreedyQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory, EpisodeParameterMemory
from rl.callbacks import FileLogger, ModelIntervalCheckpoint


ENV_NAME = 'planar_crane-v0'

LAYER_SIZE = 128
NUM_HIDDEN_LAYERS = 3
NUM_STEPS = 50000
LOG_INTERVAL = 10000
MAX_STEPS = 500
METHOD = 'DUEL_DQN' # can be DQN, DUEL_DQN, SARSA, or CEM
TRIAL_ID = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')

# Define the filenames to use for this session
WEIGHT_FILENAME = 'weights/{}_{}_weights_{}_{}_{}_{}.h5f'.format(METHOD, ENV_NAME, LAYER_SIZE, NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)
CHECKPOINT_WEIGHTS_FILENAME = 'weights/{}_{}_checkpointWeights_{{step}}_{}_{}_{}_{}.h5f'.format(METHOD, ENV_NAME, LAYER_SIZE, NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)
LOG_FILENAME = 'logs/{}_{}_log_{}_{}_{}_{}.json'.format(METHOD, ENV_NAME, LAYER_SIZE, NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)
MONITOR_FILENAME = 'example_data/{}_{}_monitor_{}_{}_{}_{}'.format(METHOD, ENV_NAME, LAYER_SIZE, NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)



# This callback will cause the eps in the EpsGreedy policy to decay over time
# As of 07/17/17, this is just a linear decrease based on epoch number
# TODO: 07/17/17 - JEV - Do something more intelligent here.
class ExploreExploit(keras.callbacks.Callback):
    NUM_EPOCHS = NUM_STEPS/MAX_STEPS # calculate the number of epochs

    def on_epoch_begin(self, epoch, logs={}):
        global agent

        try: #
            # this will return a Attribute Error if we're using BoltzmannQPolicy
            # We catch the exception and update assuming we are using BoltzmannQPolicy
            # Otherwise, we know that we are using EpsGreedyQPolicy, so we can
            # update epsilon.
            agent.policy.eps 
            agent.policy.eps = -0.9/self.NUM_EPOCHS * epoch + 1

        except(AttributeError):
            agent.policy.tau = -0.9/self.NUM_EPOCHS * epoch + 1



# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)

# Record episode data?
env.SAVE_DATA = False
env.MAX_STEPS = MAX_STEPS

# uncomment to record data about the training session, including video if video_callable is true
# env = gym.wrappers.Monitor(env, MONITOR_FILENAME, video_callable=False, force=True)

np.random.seed(123)
env.seed(123)
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

# train_policy = BoltzmannQPolicy()
train_policy = EpsGreedyQPolicy(eps=1.0)
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


callbacks = []
# callbacks += [ModelIntervalCheckpoint(CHECKPOINT_WEIGHTS_FILENAME, interval=10000)]
callbacks += [FileLogger(LOG_FILENAME, interval=100)]
# callbacks += [TensorBoard(log_dir='logs', histogram_freq=0, write_graph=True, write_images=False)]
callbacks += [ExploreExploit()]

# Optionally, we can reload a previous model's weights and continue training from there
# LOAD_WEIGHTS_FILENAME = 'weights/duel_dqn_planar_crane-v0_weights_1024_4_50000_2017-07-12_160853.h5f'
# # # Load the model weights
# agent.load_weights(LOAD_WEIGHTS_FILENAME)

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
agent.fit(env, nb_steps=NUM_STEPS, callbacks=callbacks, action_repetition=5, visualize=False, verbose=1, log_interval=LOG_INTERVAL, nb_max_episode_steps=500)

# After training is done, we save the final weights.
agent.save_weights(WEIGHT_FILENAME, overwrite=True)

# We'll also save a simply named version to make running test immediately
# following training easier. 
filename = 'weights/{}_{}_weights.h5f'.format(METHOD, ENV_NAME)
agent.save_weights(filename, overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
agent.test(env, nb_episodes=5, visualize=True,  action_repetition=5) #nb_max_episode_steps=500,
