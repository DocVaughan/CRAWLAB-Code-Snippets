#! /usr/bin/env python

###############################################################################
# tf_agents_agentEval.py
#
# Script to evaluate an PPO agent
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 01/30/20
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - @doc_vaughan
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 02/17/20 - JEV - Improve commenting
###############################################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import logging
import os
import time

import imageio
import logging
import PIL.Image

import tensorflow as tf  # pylint: disable=g-explicit-tensorflow-version-import

from tf_agents.agents.ppo import ppo_agent
from tf_agents.drivers import dynamic_episode_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.environments import parallel_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import actor_distribution_network
from tf_agents.networks import actor_distribution_rnn_network
from tf_agents.networks import value_network
from tf_agents.networks import value_rnn_network
from tf_agents.policies import policy_saver
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.utils import common

import gym


NUM_ITERATIONS = 500000
ROOT_DIR = "data_PPO"

def create_policy_eval_video(environment, py_environment, policy, filename, num_episodes=10, fps=30):
    
    filename = filename + ".mp4"

    with imageio.get_writer(filename, fps=fps) as video:
        for _ in range(num_episodes):
            time_step = environment.reset()
            video.append_data(py_environment.render())
            
            while not time_step.is_last():
                action_step = policy.action(time_step)
                time_step = environment.step(action_step.action)

                env_render = py_environment.render()

                video.append_data(env_render)

# NOTE: These parameters here must exactly match those used to train the agent.
def load_agents_and_create_videos(root_dir,
                                  env_name='CartPole-v0',
                                  env_load_fn=suite_gym.load,
                                  random_seed=None,
                                  max_ep_steps=1000,
                                  # TODO(b/127576522): rename to policy_fc_layers.
                                  actor_fc_layers=(200, 100),
                                  value_fc_layers=(200, 100),
                                  use_rnns=False,
                                  # Params for collect
                                  num_environment_steps=5000000,
                                  collect_episodes_per_iteration=1,
                                  num_parallel_environments=1,
                                  replay_buffer_capacity=10000,    # Per-environment
                                  # Params for train
                                  num_epochs=25,
                                  learning_rate=1e-3,
                                  # Params for eval
                                  num_eval_episodes=10,
                                  num_random_episodes=1,
                                  eval_interval=500,
                                  # Params for summaries and logging
                                  train_checkpoint_interval=500,
                                  policy_checkpoint_interval=500,
                                  rb_checkpoint_interval=20000,
                                  log_interval=50,
                                  summary_interval=50,
                                  summaries_flush_secs=10,
                                  use_tf_functions=True,
                                  debug_summaries=False,
                                  eval_metrics_callback=None,
                                  random_metrics_callback=None,
                                  summarize_grads_and_vars=False):
    
    root_dir = os.path.expanduser(root_dir)
    train_dir = os.path.join(root_dir, 'train')
    eval_dir = os.path.join(root_dir, 'eval')
    random_dir = os.path.join(root_dir, 'random')
    saved_model_dir = os.path.join(root_dir, 'policy_saved_model')

    train_summary_writer = tf.compat.v2.summary.create_file_writer(
            train_dir, flush_millis=summaries_flush_secs * 1000)
    train_summary_writer.set_as_default()

    eval_summary_writer = tf.compat.v2.summary.create_file_writer(
            eval_dir, flush_millis=summaries_flush_secs * 1000)
    
    eval_metrics = [
            tf_metrics.AverageReturnMetric(buffer_size=num_eval_episodes),
            tf_metrics.AverageEpisodeLengthMetric(buffer_size=num_eval_episodes)]

    random_summary_writer = tf.compat.v2.summary.create_file_writer(
            random_dir, flush_millis=summaries_flush_secs * 1000)
    
    random_metrics = [
            tf_metrics.AverageReturnMetric(buffer_size=num_eval_episodes),
            tf_metrics.AverageEpisodeLengthMetric(buffer_size=num_eval_episodes)]


    global_step = tf.compat.v1.train.get_or_create_global_step()

    if random_seed is not None:
        tf.compat.v1.set_random_seed(random_seed)
    
    eval_py_env = env_load_fn(env_name, max_episode_steps=max_ep_steps)
    eval_tf_env = tf_py_environment.TFPyEnvironment(eval_py_env)
#     tf_env = tf_py_environment.TFPyEnvironment(
#             parallel_py_environment.ParallelPyEnvironment(
#                      [lambda: env_load_fn(env_name, max_episode_steps=max_ep_steps)] * num_parallel_environments))

    tf_env = tf_py_environment.TFPyEnvironment(suite_gym.load(env_name, max_episode_steps=max_ep_steps))

    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)

    if use_rnns:
        actor_net = actor_distribution_rnn_network.ActorDistributionRnnNetwork(
                tf_env.observation_spec(),
                tf_env.action_spec(),
                input_fc_layer_params=actor_fc_layers,
                output_fc_layer_params=None)
        
        value_net = value_rnn_network.ValueRnnNetwork(
                tf_env.observation_spec(),
                input_fc_layer_params=value_fc_layers,
                output_fc_layer_params=None)
    
    else:
        actor_net = actor_distribution_network.ActorDistributionNetwork(
                tf_env.observation_spec(),
                tf_env.action_spec(),
                fc_layer_params=actor_fc_layers,
                activation_fn=tf.keras.activations.tanh)
        
        value_net = value_network.ValueNetwork(
                tf_env.observation_spec(),
                fc_layer_params=value_fc_layers,
                activation_fn=tf.keras.activations.tanh)

    tf_agent = ppo_agent.PPOAgent(
            tf_env.time_step_spec(),
            tf_env.action_spec(),
            optimizer,
            actor_net=actor_net,
            value_net=value_net,
            entropy_regularization=0.0,
            importance_ratio_clipping=0.2,
            normalize_observations=False,
            normalize_rewards=False,
            use_gae=True,
            kl_cutoff_factor=0.0,
            initial_adaptive_kl_beta=0.0,
            num_epochs=num_epochs,
            debug_summaries=debug_summaries,
            summarize_grads_and_vars=summarize_grads_and_vars,
            train_step_counter=global_step)
    
    tf_agent.initialize()

    environment_steps_metric = tf_metrics.EnvironmentSteps()
    
    step_metrics = [tf_metrics.NumberOfEpisodes(),
                    environment_steps_metric,]

    train_metrics = step_metrics + [
            tf_metrics.AverageReturnMetric(
                    batch_size=num_parallel_environments),
            tf_metrics.AverageEpisodeLengthMetric(
                    batch_size=num_parallel_environments),]

    eval_policy = tf_agent.policy
    collect_policy = tf_agent.collect_policy

    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
            tf_agent.collect_data_spec,
            batch_size=num_parallel_environments,
            max_length=replay_buffer_capacity)

    train_checkpointer = common.Checkpointer(
            ckpt_dir=train_dir,
            agent=tf_agent,
            global_step=global_step,
            metrics=metric_utils.MetricsGroup(train_metrics, 'train_metrics'))
    
    policy_checkpointer = common.Checkpointer(
            ckpt_dir=os.path.join(train_dir, 'policy'),
            policy=eval_policy,
            global_step=global_step)
    
    rb_checkpointer = common.Checkpointer(
            ckpt_dir=os.path.join(train_dir, 'replay_buffer'),
            max_to_keep=1,
            replay_buffer=replay_buffer)
    
    saved_model = policy_saver.PolicySaver(
            eval_policy, train_step=global_step)

    train_checkpointer.initialize_or_restore()
    rb_checkpointer.initialize_or_restore()

    collect_driver = dynamic_episode_driver.DynamicEpisodeDriver(
            tf_env,
            collect_policy,
            observers=[replay_buffer.add_batch] + train_metrics,
            num_episodes=collect_episodes_per_iteration)

    # if use_tf_functions:
    #     # To speed up collect use common.function.
    #     collect_driver.run = common.function(collect_driver.run)
    #     tf_agent.train = common.function(tf_agent.train)

    # initial_collect_policy = random_tf_policy.RandomTFPolicy(
    #         tf_env.time_step_spec(), tf_env.action_spec())

    random_policy = random_tf_policy.RandomTFPolicy(eval_tf_env.time_step_spec(),
                                                    eval_tf_env.action_spec())

    # Make movies of the trained agent and a random agent
    date_string = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    
    trained_filename = "trainedPPO_" + date_string
    create_policy_eval_video(eval_tf_env, eval_py_env, tf_agent.policy, trained_filename)

    random_filename = 'random_' + date_string
    create_policy_eval_video(eval_tf_env, eval_py_env, random_policy, random_filename)

def main():
    tf.compat.v1.enable_v2_behavior()
    logging.basicConfig(level=logging.INFO)
    load_agents_and_create_videos(ROOT_DIR)

if __name__ == '__main__':
    main()

