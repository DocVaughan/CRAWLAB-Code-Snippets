#! /usr/bin/env python

###############################################################################
# openAI_variableLengthPendulum_learning.py
#
# Simple Q-learning setup for the variable length pendulum
#
# Extended/reworked from:
#  https://keon.io/deep-q-learning/
#  https://github.com/keon/deep-q-learning
#
# Also see:
#  https://github.com/matthiasplappert/keras-rl
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

import numpy as np
import matplotlib.pyplot as plt

import gym
import random
import time
import variable_pendulum

from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

EPISODES = 1000

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    
        self.epsilon = 1.0  
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
              target = reward + self.gamma * \
                       np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


if __name__ == "__main__":
    env = gym.make('variable_pendulum-v0')
    
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    # agent.load("./save/cartpole-master.h5")
    done = False
    batch_size = 32
  
    for e in range(EPISODES):
        state = env.reset()
        state = np.reshape(state, [1, 4])
  
        for time_t in range(500):
            if e % 100 == 0: # render every 100th episode - slow
                env.render()

            action = agent.act(state)
  
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, 4])

            agent.remember(state, action, reward, next_state, done)
            state = next_state

            if done:                
                print("episode: {}/{}, score: {}"
                      .format(e, EPISODES, time_t))
                break
        
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)