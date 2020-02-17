#! /usr/bin/env python

###############################################################################
# TF_agents_DQN.py
#
# A simple DQN agent using the tf-agents library, patterned after that at:
#    https://github.com/tensorflow/agents/blob/master/tf_agents/agents/dqn/examples/v2/train_eval.py
#
# The license from that file is included below.
#
# It does include callbacks that are compatible with viewing training progress on 
# Tensorboard. To view, once this script is running (and assuming the default ROOT_DIR 
# is used), from a second terminal run:
#
#  tensorboard --logdir path_to_this_script_folder/data_DQN --port 2223
#
# where path_to_this_script_folder is the absolute path to the folder that contains this
# script. Once that is run, go to a web browser and address:
#
#  0.0.0.0:2223
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
#   * 02/17/20 - JEV - test recurrent/LSTM version
#   * 02/17/20 - JEV - Improve commenting
###############################################################################

# coding=utf-8
# Copyright 2018 The TF-Agents Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python2, python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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


NUM_ITERATIONS = 5000000
ROOT_DIR = "data"

def train_eval(
        root_dir,
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
    
    
    # Set up the directories to contain the log data and model saves 
    # If data already exist in these folders, then we will try to load it later.
    train_dir = os.path.join(root_dir, 'train')
    eval_dir = os.path.join(root_dir, 'eval')
    random_dir = os.path.join(root_dir, 'random')

    # Create writers for logging and specify the metrics to log for each
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

    # Set up the agent and train, recoding data at each summary_internal number of steps
    with tf.compat.v2.summary.record_if(
            lambda: tf.math.equal(global_step % summary_interval, 0)):

        # Load the environments. Here, we used the same for evaluation and training. 
        # However, they could be different.
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
                # tf_metrics.NumberOfEpisodes(),
                # tf_metrics.EnvironmentSteps(),
                tf_metrics.AverageReturnMetric(),
                tf_metrics.AverageEpisodeLengthMetric(),]

        eval_policy = tf_agent.policy
        collect_policy = tf_agent.collect_policy

        replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
                data_spec=tf_agent.collect_data_spec,
                batch_size=tf_env.batch_size,
                max_length=replay_buffer_capacity)

        collect_driver = dynamic_step_driver.DynamicStepDriver(
                tf_env,
                collect_policy,
                observers=[replay_buffer.add_batch] + train_metrics,
                num_steps=collect_steps_per_iteration)

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

        train_checkpointer.initialize_or_restore()
        rb_checkpointer.initialize_or_restore()

        if use_tf_functions:
            # To speed up collect use common.function.
            collect_driver.run = common.function(collect_driver.run)
            tf_agent.train = common.function(tf_agent.train)

        initial_collect_policy = random_tf_policy.RandomTFPolicy(
                tf_env.time_step_spec(), tf_env.action_spec())

        random_policy = random_tf_policy.RandomTFPolicy(eval_tf_env.time_step_spec(),
                                                        eval_tf_env.action_spec())

        # Collect initial replay data.
        logging.info(
                'Initializing replay buffer by collecting experience for %d steps with '
                'a random policy.', initial_collect_steps)
        
        dynamic_step_driver.DynamicStepDriver(
                tf_env,
                initial_collect_policy,
                observers=[replay_buffer.add_batch] + train_metrics,
                num_steps=initial_collect_steps).run()

        results = metric_utils.eager_compute(
                eval_metrics,
                eval_tf_env,
                eval_policy,
                num_episodes=num_eval_episodes,
                train_step=global_step,
                summary_writer=eval_summary_writer,
                summary_prefix='Metrics',)

        if eval_metrics_callback is not None:
            eval_metrics_callback(results, global_step.numpy())
        
        metric_utils.log_metrics(eval_metrics)

        time_step = None
        policy_state = collect_policy.get_initial_state(tf_env.batch_size)

        timed_at_step = global_step.numpy()
        time_acc = 0

        # Dataset generates trajectories with shape [Bx2x...]
        dataset = replay_buffer.as_dataset(
                num_parallel_calls=3,
                sample_batch_size=batch_size,
                num_steps=train_sequence_length + 1).prefetch(3)
        
        iterator = iter(dataset)

        def train_step():
            experience, _ = next(iterator)
            return tf_agent.train(experience)

        if use_tf_functions:
            train_step = common.function(train_step)
        

        for _ in range(num_iterations):
            start_time = time.time()
            time_step, policy_state = collect_driver.run(time_step=time_step,
                                                         policy_state=policy_state,)
        
            for _ in range(train_steps_per_iteration):
                train_loss = train_step()
        
            time_acc += time.time() - start_time

            if global_step.numpy() % log_interval == 0:
                logging.info('Step: {:>6d}\tLoss: {:>+20.4f}'.format(global_step.numpy(),
                                                                     train_loss.loss))

                steps_per_sec = (global_step.numpy() - timed_at_step) / time_acc
                logging.info('{:6.3f} steps/sec'.format(steps_per_sec))
            
                tf.compat.v2.summary.scalar(name='global_steps_per_sec', 
                                            data=steps_per_sec, 
                                            step=global_step)

                timed_at_step = global_step.numpy()
                time_acc = 0

            for train_metric in train_metrics:
                train_metric.tf_summaries(
                        train_step=global_step, step_metrics=train_metrics[:2])

            if global_step.numpy() % train_checkpoint_interval == 0:
                train_checkpointer.save(global_step=global_step.numpy())

            if global_step.numpy() % policy_checkpoint_interval == 0:
                policy_checkpointer.save(global_step=global_step.numpy())

            if global_step.numpy() % rb_checkpoint_interval == 0:
                rb_checkpointer.save(global_step=global_step.numpy())

            if global_step.numpy() % eval_interval == 0:
                results = metric_utils.eager_compute(
                        eval_metrics,
                        eval_tf_env,
                        eval_policy,
                        num_episodes=num_eval_episodes,
                        train_step=global_step,
                        summary_writer=eval_summary_writer,
                        summary_prefix='Metrics',)
            
                if eval_metrics_callback is not None:
                    eval_metrics_callback(results, global_step.numpy())
            
                metric_utils.log_metrics(eval_metrics)

                random_results = metric_utils.eager_compute(
                        random_metrics,
                        eval_tf_env,
                        random_policy,
                        num_episodes=num_random_episodes,
                        train_step=global_step,
                        summary_writer=random_summary_writer,
                        summary_prefix='Metrics',)
            
                if random_metrics_callback is not None:
                    random_metrics_callback(random_results, global_step.numpy())
            
                metric_utils.log_metrics(random_metrics)

        return train_loss


def main():
    tf.compat.v1.enable_v2_behavior()
    logging.basicConfig(level=logging.INFO)
    train_eval(ROOT_DIR, num_iterations=NUM_ITERATIONS)

if __name__ == '__main__':
    main()