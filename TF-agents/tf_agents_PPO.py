##############################################################################
# TF_agents_PPO.py
#
# A simple PPO agent using the tf-agents library, patterned after that at:
#    https://github.com/tensorflow/agents/blob/master/tf_agents/agents/dqn/examples/v2/train_eval.py
#
# The license from that file is included below.
#
# It does include callbacks that are compatible with viewing training progress on 
# Tensorboard. To view, once this script is running (and assuming the default ROOT_DIR 
# is used), from a second terminal run:
#
#  tensorboard --logdir path_to_this_script_folder/data_PPO --port 2223
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

r"""Train and Eval PPO.

To run:

```bash
tensorboard --logdir $HOME/tmp/ppo/gym/HalfCheetah-v2/ --port 2223 &

python tf_agents/agents/ppo/examples/v2/train_eval.py \
    --root_dir=$HOME/tmp/ppo/gym/HalfCheetah-v2/ \
    --logtostderr
```
"""

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

from tf_agents.agents.ppo import ppo_agent
from tf_agents.drivers import dynamic_episode_driver
from tf_agents.environments import parallel_py_environment
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
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

def train_eval(
        root_dir,
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
    
    
    # Set up the directories to contain the log data and model saves 
    # If data already exist in these folders, then we will try to load it later.
    if root_dir is None:
        raise AttributeError('train_eval requires a root_dir.')

    root_dir = os.path.expanduser(root_dir)
    train_dir = os.path.join(root_dir, 'train')
    eval_dir = os.path.join(root_dir, 'eval')
    random_dir = os.path.join(root_dir, 'random')
    saved_model_dir = os.path.join(root_dir, 'policy_saved_model')

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
        
        if random_seed is not None:
            tf.compat.v1.set_random_seed(random_seed)
        
        # Load the environments. Here, we used the same for evaluation and training. 
        # However, they could be different.
        eval_tf_env = tf_py_environment.TFPyEnvironment(env_load_fn(env_name, max_episode_steps=max_ep_steps))
        # tf_env = tf_py_environment.TFPyEnvironment(
        #         parallel_py_environment.ParallelPyEnvironment(
        #                 [lambda: env_load_fn(env_name, max_episode_steps=max_ep_steps)] * num_parallel_environments))

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

        def train_step():
            trajectories = replay_buffer.gather_all()
            return tf_agent.train(experience=trajectories)

        if use_tf_functions:
            # TODO(b/123828980): Enable once the cause for slowdown was identified.
            collect_driver.run = common.function(collect_driver.run, autograph=False)
            tf_agent.train = common.function(tf_agent.train, autograph=False)
            train_step = common.function(train_step)

        random_policy = random_tf_policy.RandomTFPolicy(eval_tf_env.time_step_spec(),
                                                        eval_tf_env.action_spec())

        collect_time = 0
        train_time = 0
        timed_at_step = global_step.numpy()

        while environment_steps_metric.result() < num_environment_steps:
            global_step_val = global_step.numpy()
            
            if global_step_val % eval_interval == 0:
                metric_utils.eager_compute(eval_metrics,
                                           eval_tf_env,
                                           eval_policy,
                                           num_episodes=num_eval_episodes,
                                           train_step=global_step,
                                           summary_writer=eval_summary_writer,
                                           summary_prefix='Metrics',)

                metric_utils.eager_compute(random_metrics,
                                           eval_tf_env,
                                           random_policy,
                                           num_episodes=num_random_episodes,
                                           train_step=global_step,
                                           summary_writer=random_summary_writer,
                                           summary_prefix='Metrics',)

            start_time = time.time()
            collect_driver.run()
            collect_time += time.time() - start_time

            start_time = time.time()
            total_loss, _ = train_step()
            replay_buffer.clear()
            train_time += time.time() - start_time

            for train_metric in train_metrics:
                train_metric.tf_summaries(
                        train_step=global_step, step_metrics=step_metrics)

            if global_step_val % log_interval == 0:
                logging.info('Step: {:>6d}\tLoss: {:>+20.4f}'.format(global_step_val, 
                                                              total_loss))
                
                steps_per_sec = (
                        (global_step_val - timed_at_step) / (collect_time + train_time))
                
                logging.info('{:6.3f} steps/sec'.format(steps_per_sec))
                logging.info('collect_time = {:.3f}, train_time = {:.3f}'.format(collect_time,
                                                                                 train_time))
               
                with tf.compat.v2.summary.record_if(True):
                    tf.compat.v2.summary.scalar(name='global_steps_per_sec', 
                                            data=steps_per_sec, 
                                            step=global_step)

            if global_step_val % train_checkpoint_interval == 0:
                train_checkpointer.save(global_step=global_step_val)

            if global_step_val % policy_checkpoint_interval == 0:
                policy_checkpointer.save(global_step=global_step_val)
                saved_model_path = os.path.join(
                        saved_model_dir, 'policy_' + ('%d' % global_step_val).zfill(9))
                saved_model.save(saved_model_path)
            
            if global_step_val % rb_checkpoint_interval == 0:
                rb_checkpointer.save(global_step=global_step.numpy())

            timed_at_step = global_step_val
            collect_time = 0
            train_time = 0

        # One final eval before exiting.
        metric_utils.eager_compute(eval_metrics,
                                   eval_tf_env,
                                   eval_policy,
                                   num_episodes=num_eval_episodes,
                                   train_step=global_step,
                                   summary_writer=eval_summary_writer,
                                   summary_prefix='Metrics',)

def main():
    logging.basicConfig(level=logging.INFO)
    tf.compat.v1.enable_v2_behavior()
    train_eval(ROOT_DIR)


if __name__ == '__main__':
    main()