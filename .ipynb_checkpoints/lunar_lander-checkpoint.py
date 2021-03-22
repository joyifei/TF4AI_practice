{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "import environment\n",
    "from utils import get_landing_zone, get_angle, get_velocity, get_position, get_fuel, tests\n",
    "get_landing_zone()\n",
    "# Lunar Lander Environment\n",
    "class LunarLanderEnvironment(environment.BaseEnvironment):\n",
    "    def __init__(self):\n",
    "        self.current_state = None\n",
    "        self.count = 0\n",
    "    \n",
    "    def env_init(self, env_info):\n",
    "        # users set this up\n",
    "        self.state = np.zeros(6) # velocity x, y, angle, distance to ground, landing zone x, y\n",
    "    \n",
    "    def env_start(self):\n",
    "        land_x, land_y = get_landing_zone() # gets the x, y coordinate of the landing zone\n",
    "        # At the start we initialize the agent to the top left hand corner (100, 20) with 0 velocity \n",
    "        # in either any direction. The agent's angle is set to 0 and the landing zone is retrieved and set.\n",
    "        # The lander starts with fuel of 100.\n",
    "        # (vel_x, vel_y, angle, pos_x, pos_y, land_x, land_y, fuel)\n",
    "        self.current_state = (0, 0, 0, 100, 20, land_x, land_y, 100)\n",
    "        print( self.current_state )\n",
    "        return self.current_state\n",
    "    \n",
    "    def env_step(self, action):\n",
    "        \n",
    "        land_x, land_y = get_landing_zone() # gets the x, y coordinate of the landing zone\n",
    "        vel_x, vel_y = get_velocity(action) # gets the x, y velocity of the lander\n",
    "        angle = get_angle(action) # gets the angle the lander is positioned in\n",
    "        pos_x, pos_y = get_position(action) # gets the x, y position of the lander\n",
    "        fuel = get_fuel(action) # get the amount of fuel remaining for the lander\n",
    "        \n",
    "        terminal = False\n",
    "        reward = 0.0\n",
    "        observation = (vel_x, vel_y, angle, pos_x, pos_y, land_x, land_y, fuel)\n",
    "        \n",
    "        # use the above observations to decide what the reward will be, and if the\n",
    "        # agent is in a terminal state.\n",
    "        # Recall - if the agent crashes or lands terminal needs to be set to True\n",
    "        print( observation )\n",
    "        # YOUR CODE HERE\n",
    "        crashed = False;\n",
    "        landed = False\n",
    "        if pos_y <= land_y:\n",
    "            terminal = True\n",
    "            landed = True\n",
    "            if vel_y < -3 or vel_x < -10 or vel_x > 10 or ( angle > 5 and angle < 355 ) or pos_x != land_x:\n",
    "                crashed = True\n",
    "        elif fuel <= 0:\n",
    "            terminal = True\n",
    "            crashed = True\n",
    "       \n",
    "        if crashed :\n",
    "            reward = -10000\n",
    "        elif landed:\n",
    "            reward = reward + 1000\n",
    "            reward += fuel\n",
    "        \n",
    "        \n",
    "            \n",
    "        landed_successfully = landed and not crashed\n",
    "        print( ' is landed: ', landed, ' is crashed: ', crashed, ' fuel: ', fuel )\n",
    "        #raise NotImplementedError()\n",
    "        \n",
    "        self.reward_obs_term = (reward, observation, terminal)\n",
    "        return self.reward_obs_term\n",
    "    \n",
    "    def env_cleanup(self):\n",
    "        return None\n",
    "    \n",
    "    def env_message(self):\n",
    "        return None"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(0, 0, 0, 100, 20, 50, 0, 100)\n",
      "(0, 0, 0, 2, 0, 50, 0, 10)\n",
      " is landed:  True  is crashed:  True  fuel:  10\n",
      "Reward: -10000, Terminal: True\n"
     ]
    }
   ],
   "source": [
    "tests( LunarLanderEnvironment, 5 )"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
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
