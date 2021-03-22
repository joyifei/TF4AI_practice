{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#!/usr/bin/env python\n",
    "\n",
    "\"\"\"Glues together an experiment, agent, and environment.\n",
    "\"\"\"\n",
    "\n",
    "from __future__ import print_function\n",
    "\n",
    "\n",
    "class RLGlue:\n",
    "    \"\"\"RLGlue class\n",
    "\n",
    "    args:\n",
    "        env_name (string): the name of the module where the Environment class can be found\n",
    "        agent_name (string): the name of the module where the Agent class can be found\n",
    "    \"\"\"\n",
    "\n",
    "    def __init__(self, env_class, agent_class):\n",
    "        self.environment = env_class()\n",
    "        self.agent = agent_class()\n",
    "\n",
    "        self.total_reward = None\n",
    "        self.last_action = None\n",
    "        self.num_steps = None\n",
    "        self.num_episodes = None\n",
    "\n",
    "    def rl_init(self, agent_init_info={}, env_init_info={}):\n",
    "        \"\"\"Initial method called when RLGlue experiment is created\"\"\"\n",
    "        self.environment.env_init(env_init_info)\n",
    "        self.agent.agent_init(agent_init_info)\n",
    "\n",
    "        self.total_reward = 0.0\n",
    "        self.num_steps = 0\n",
    "        self.num_episodes = 0\n",
    "\n",
    "    def rl_start(self, agent_start_info={}, env_start_info={}):\n",
    "        \"\"\"Starts RLGlue experiment\n",
    "\n",
    "        Returns:\n",
    "            tuple: (state, action)\n",
    "        \"\"\"\n",
    "        \n",
    "        self.total_reward = 0.0\n",
    "        self.num_steps = 1\n",
    "\n",
    "        last_state = self.environment.env_start()\n",
    "        self.last_action = self.agent.agent_start(last_state)\n",
    "\n",
    "        observation = (last_state, self.last_action)\n",
    "\n",
    "        return observation\n",
    "\n",
    "    def rl_agent_start(self, observation):\n",
    "        \"\"\"Starts the agent.\n",
    "\n",
    "        Args:\n",
    "            observation: The first observation from the environment\n",
    "\n",
    "        Returns:\n",
    "            The action taken by the agent.\n",
    "        \"\"\"\n",
    "        return self.agent.agent_start(observation)\n",
    "\n",
    "    def rl_agent_step(self, reward, observation):\n",
    "        \"\"\"Step taken by the agent\n",
    "\n",
    "        Args:\n",
    "            reward (float): the last reward the agent received for taking the\n",
    "                last action.\n",
    "            observation : the state observation the agent receives from the\n",
    "                environment.\n",
    "\n",
    "        Returns:\n",
    "            The action taken by the agent.\n",
    "        \"\"\"\n",
    "        return self.agent.agent_step(reward, observation)\n",
    "\n",
    "    def rl_agent_end(self, reward):\n",
    "        \"\"\"Run when the agent terminates\n",
    "\n",
    "        Args:\n",
    "            reward (float): the reward the agent received when terminating\n",
    "        \"\"\"\n",
    "        self.agent.agent_end(reward)\n",
    "\n",
    "    def rl_env_start(self):\n",
    "        \"\"\"Starts RL-Glue environment.\n",
    "\n",
    "        Returns:\n",
    "            (float, state, Boolean): reward, state observation, boolean\n",
    "                indicating termination\n",
    "        \"\"\"\n",
    "        self.total_reward = 0.0\n",
    "        self.num_steps = 1\n",
    "\n",
    "        this_observation = self.environment.env_start()\n",
    "\n",
    "        return this_observation\n",
    "\n",
    "    def rl_env_step(self, action):\n",
    "        \"\"\"Step taken by the environment based on action from agent\n",
    "\n",
    "        Args:\n",
    "            action: Action taken by agent.\n",
    "\n",
    "        Returns:\n",
    "            (float, state, Boolean): reward, state observation, boolean\n",
    "                indicating termination.\n",
    "        \"\"\"\n",
    "        ro = self.environment.env_step(action)\n",
    "        (this_reward, _, terminal) = ro\n",
    "\n",
    "        self.total_reward += this_reward\n",
    "\n",
    "        if terminal:\n",
    "            self.num_episodes += 1\n",
    "        else:\n",
    "            self.num_steps += 1\n",
    "\n",
    "        return ro\n",
    "\n",
    "    def rl_step(self):\n",
    "        \"\"\"Step taken by RLGlue, takes environment step and either step or\n",
    "            end by agent.\n",
    "\n",
    "        Returns:\n",
    "            (float, state, action, Boolean): reward, last state observation,\n",
    "                last action, boolean indicating termination\n",
    "        \"\"\"\n",
    "\n",
    "        (reward, last_state, term) = self.environment.env_step(self.last_action)\n",
    "\n",
    "        self.total_reward += reward;\n",
    "\n",
    "        if term:\n",
    "            self.num_episodes += 1\n",
    "            self.agent.agent_end(reward)\n",
    "            roat = (reward, last_state, None, term)\n",
    "        else:\n",
    "            self.num_steps += 1\n",
    "            self.last_action = self.agent.agent_step(reward, last_state)\n",
    "            roat = (reward, last_state, self.last_action, term)\n",
    "\n",
    "        return roat\n",
    "\n",
    "    def rl_cleanup(self):\n",
    "        \"\"\"Cleanup done at end of experiment.\"\"\"\n",
    "        self.environment.env_cleanup()\n",
    "        self.agent.agent_cleanup()\n",
    "\n",
    "    def rl_agent_message(self, message):\n",
    "        \"\"\"Message passed to communicate with agent during experiment\n",
    "\n",
    "        Args:\n",
    "            message: the message (or question) to send to the agent\n",
    "\n",
    "        Returns:\n",
    "            The message back (or answer) from the agent\n",
    "\n",
    "        \"\"\"\n",
    "\n",
    "        return self.agent.agent_message(message)\n",
    "\n",
    "    def rl_env_message(self, message):\n",
    "        \"\"\"Message passed to communicate with environment during experiment\n",
    "\n",
    "        Args:\n",
    "            message: the message (or question) to send to the environment\n",
    "\n",
    "        Returns:\n",
    "            The message back (or answer) from the environment\n",
    "\n",
    "        \"\"\"\n",
    "        return self.environment.env_message(message)\n",
    "\n",
    "    def rl_episode(self, max_steps_this_episode):\n",
    "        \"\"\"Runs an RLGlue episode\n",
    "\n",
    "        Args:\n",
    "            max_steps_this_episode (Int): the maximum steps for the experiment to run in an episode\n",
    "\n",
    "        Returns:\n",
    "            Boolean: if the episode should terminate\n",
    "        \"\"\"\n",
    "        is_terminal = False\n",
    "\n",
    "        self.rl_start()\n",
    "\n",
    "        while (not is_terminal) and ((max_steps_this_episode == 0) or\n",
    "                                     (self.num_steps < max_steps_this_episode)):\n",
    "            rl_step_result = self.rl_step()\n",
    "            is_terminal = rl_step_result[3]\n",
    "\n",
    "        return is_terminal\n",
    "\n",
    "    def rl_return(self):\n",
    "        \"\"\"The total reward\n",
    "\n",
    "        Returns:\n",
    "            float: the total reward\n",
    "        \"\"\"\n",
    "        return self.total_reward\n",
    "\n",
    "    def rl_num_steps(self):\n",
    "        \"\"\"The total number of steps taken\n",
    "\n",
    "        Returns:\n",
    "            Int: the total number of steps taken\n",
    "        \"\"\"\n",
    "        return self.num_steps\n",
    "\n",
    "    def rl_num_episodes(self):\n",
    "        \"\"\"The number of episodes\n",
    "\n",
    "        Returns\n",
    "            Int: the total number of episodes\n",
    "\n",
    "        \"\"\"\n",
    "        return self.num_episodes\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
