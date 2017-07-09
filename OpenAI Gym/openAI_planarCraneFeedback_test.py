import numpy as np
import gym
import planar_crane_feedback

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy, GreedyQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory


ENV_NAME = 'planar_crane_feedback-v0'
FILENAME = 'dqn_planar_crane_feedback-v0_weights.h5f'

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.n

LAYER_SIZE = 128
NUM_STEPS = 1000000

# Next, we build a very simple model.
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(LAYER_SIZE))
model.add(Activation('relu'))
model.add(Dense(LAYER_SIZE))
model.add(Activation('relu'))
model.add(Dense(LAYER_SIZE))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=NUM_STEPS, window_length=1)
train_policy = BoltzmannQPolicy(tau=0.05)
test_policy = GreedyQPolicy()
# test_policy = EpsGreedyQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
               target_model_update=1e-2, policy=train_policy, test_policy=test_policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Load the model weights
dqn.load_weights(FILENAME)

# Finally, evaluate our algorithm for 1 episode.
dqn.test(env, nb_episodes=5, visualize=True, nb_max_episode_steps=500)