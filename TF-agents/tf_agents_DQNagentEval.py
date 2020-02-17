#! /usr/bin/env python

###############################################################################
# tf_agents_agentEval.py
#
# Script to evaluate a DQN agent
#
# NOTE: Any plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Created: 02/17/20
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

from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import q_network
from tf_agents.networks import q_rnn_network
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.utils import common

import gym


NUM_ITERATIONS = 500000
ROOT_DIR = "data"

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
        num_iterations=NUM_ITERATIONS,
        max_ep_steps=1000,
        train_sequence_length=1,
        # Params for QNetwork
        fc_layer_params=((128,64,32)),
        # Params for QRnnNetwork
        input_fc_layer_params=(50,),
        lstm_size=(20,),
        output_fc_layer_params=(20,),
        # Params for collect
        initial_collect_steps=1000,
        collect_steps_per_iteration=1,
        epsilon_greedy=0.1,
        replay_buffer_capacity=10000,
        # Params for target update
        target_update_tau=0.05,
        target_update_period=5,
        # Params for train
        train_steps_per_iteration=1,
        batch_size=64,
        learning_rate=1e-3,
        n_step_update=1,
        gamma=0.99,
        reward_scale_factor=1.0,
        gradient_clipping=None,
        use_tf_functions=True,
        # Params for eval 
        num_eval_episodes=10,
        num_random_episodes=1,
        eval_interval=1000,
        # Params for checkpoints
        train_checkpoint_interval=10000,
        policy_checkpoint_interval=5000,
        rb_checkpoint_interval=20000,
        # Params for summaries and logging
        log_interval=1000,
        summary_interval=1000,
        summaries_flush_secs=10,
        debug_summaries=False,
        summarize_grads_and_vars=False,
        eval_metrics_callback=None,
        random_metrics_callback=None):
    
    
    
    train_dir = os.path.join(root_dir, 'train')
    eval_dir = os.path.join(root_dir, 'eval')
    random_dir = os.path.join(root_dir, 'random')
    
    eval_metrics = [
            tf_metrics.AverageReturnMetric(buffer_size=num_eval_episodes),
            tf_metrics.AverageEpisodeLengthMetric(buffer_size=num_eval_episodes)]

    global_step = tf.compat.v1.train.get_or_create_global_step()
    
    # Match the environments used in training
    tf_env = tf_py_environment.TFPyEnvironment(suite_gym.load(env_name, max_episode_steps=max_ep_steps))
    eval_py_env = suite_gym.load(env_name, max_episode_steps=max_ep_steps)
    eval_tf_env = tf_py_environment.TFPyEnvironment(eval_py_env)

    if train_sequence_length != 1 and n_step_update != 1:
        raise NotImplementedError(
                'train_eval does not currently support n-step updates with stateful '
                'networks (i.e., RNNs)')

    if train_sequence_length > 1:
        q_net = q_rnn_network.QRnnNetwork(
                tf_env.observation_spec(),
                tf_env.action_spec(),
                input_fc_layer_params=input_fc_layer_params,
                lstm_size=lstm_size,
                output_fc_layer_params=output_fc_layer_params)
    else:
        q_net = q_network.QNetwork(
                tf_env.observation_spec(),
                tf_env.action_spec(),
                fc_layer_params=fc_layer_params)

        train_sequence_length = n_step_update

    # Match the agents used in training
    tf_agent = dqn_agent.DqnAgent(
            tf_env.time_step_spec(),
            tf_env.action_spec(),
            q_network=q_net,
            epsilon_greedy=epsilon_greedy,
            n_step_update=n_step_update,
            target_update_tau=target_update_tau,
            target_update_period=target_update_period,
            optimizer=tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate),
            td_errors_loss_fn=common.element_wise_squared_loss,
            gamma=gamma,
            reward_scale_factor=reward_scale_factor,
            gradient_clipping=gradient_clipping,
            debug_summaries=debug_summaries,
            summarize_grads_and_vars=summarize_grads_and_vars,
            train_step_counter=global_step)
    
    tf_agent.initialize()

    train_metrics = [
            tf_metrics.NumberOfEpisodes(),
            tf_metrics.EnvironmentSteps(),
            tf_metrics.AverageReturnMetric(),
            tf_metrics.AverageEpisodeLengthMetric(),]

    eval_policy = tf_agent.policy

    replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
            data_spec=tf_agent.collect_data_spec,
            batch_size=tf_env.batch_size,
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

    # Load the data from training
    train_checkpointer.initialize_or_restore()
    rb_checkpointer.initialize_or_restore()

    # Define a random policy for comparison
    random_policy = random_tf_policy.RandomTFPolicy(eval_tf_env.time_step_spec(),
                                                    eval_tf_env.action_spec())

    # Make movies of the trained agent and a random agent
    date_string = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    
    trained_filename = "trained-agent" + date_string
    create_policy_eval_video(eval_tf_env, eval_py_env, tf_agent.policy, trained_filename)

    random_filename = 'random-agent ' + date_string
    create_policy_eval_video(eval_tf_env, eval_py_env, random_policy, random_filename)

def main():
    tf.compat.v1.enable_v2_behavior()
    logging.basicConfig(level=logging.INFO)
    load_agents_and_create_videos(ROOT_DIR)

if __name__ == '__main__':
    main()

