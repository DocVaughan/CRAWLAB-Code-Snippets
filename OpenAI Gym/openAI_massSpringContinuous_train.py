#! /usr/bin/env python

###############################################################################
# openAI_massSpringContinuous_train.py
#
# File to train on the CRAWLAB custom OpenAI mass spring damper environment 
#
# Requires:
#  * CRAWLAB mass_spring_damper_continuous Open_AI environment folder to be in the same as this file
#  * keras, openAI gym, keras-rl packages (all are pip or conda installable)
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
#   * Add GUI file picker or CLI argument parser for weight filename
###############################################################################

import numpy as np
import datetime     # used to generate unique filenames

import gym
import mass_spring_damper_continuous

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, merge
from keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess
from rl.callbacks import FileLogger, ModelIntervalCheckpoint


ENV_NAME = 'mass_spring_damper_continuous-v0'

LAYER_SIZE = 512
NUM_HIDDEN_LAYERS = 3
NUM_STEPS = 1000000
TRIAL_ID = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.shape[0]

# Record episode data?
env.SAVE_DATA = False
env.MAX_STEPS = 500

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


# critic model - TODO: 07/14/17 - update this to sequential model style
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
# random_process = OrnsteinUhlenbeckProcess(size=nb_actions, dt = env.tau, theta=1.0, mu=0.0, sigma=0.5, sigma_min=0.3, n_steps_annealing=NUM_STEPS)

agent = DDPGAgent(nb_actions=nb_actions, actor=actor, critic=critic, critic_action_input=action_input,
                  memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100,
                  random_process=random_process, gamma=.999, target_model_update=1e-3,
                  delta_clip=1.0)

agent.compile(Adam(lr=3e-4, clipnorm=1.0), metrics=['mae'])




# Optionally, we can reload a previous model's weights and continue training from there
# Remove the _actor or _critic from the filename. The load method automatically
# appends these.        
WEIGHTS_FILENAME = 'weights/ddpg_{}_weights.h5f'.format(ENV_NAME)
# agent.load_weights(WEIGHTS_FILENAME)


callbacks = []
checkpoint_weights_filename = 'weights/ddpg_{}_checkpointWeights_{{step}}_{}_{}_{}_{}.h5f'.format(ENV_NAME, LAYER_SIZE, NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)
log_filename = 'logs/ddpg_{}_log_{}_{}_{}_{}.json'.format(ENV_NAME, LAYER_SIZE, NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)
#callbacks += [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=100000)]
callbacks += [FileLogger(log_filename, interval=100)]

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
agent.fit(env, nb_steps=NUM_STEPS, callbacks=callbacks, visualize=False, verbose=1, action_repetition=5)#, nb_max_episode_steps=500)

# After training is done, we save the final weights.
filename = 'weights/ddpg_{}_weights_{}_{}_{}_{}.h5f'.format(ENV_NAME, LAYER_SIZE, NUM_HIDDEN_LAYERS, NUM_STEPS, TRIAL_ID)
agent.save_weights(filename, overwrite=True)

# We'll also save a simply named version to make running test immediately
# following training easier. 
filename = 'weights/ddpg_{}_weights.h5f'.format(ENV_NAME)
agent.save_weights(filename, overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
# agent.test(env, visualize=True) #nb_max_episode_steps=500,
