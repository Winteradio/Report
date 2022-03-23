import gym
import numpy as numpy
import random
import os
import time

ALPHA = 0.4
GAMMA = 0.9
EPSILON = 0.1
TIMES = 10000000

env = gym.make("Taxi-vi")

actions = env.action_space.n
print(actions)