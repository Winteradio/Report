import gym
import numpy as np
import random
import os
import time

ALPHA = 0.4
GAMMA = 0.9
EPSILON = 0.1
TIMEs = 10000000
## 타임 스탭을 천만 법 실행

env = gym.make("Taxi-vi")

actions = env.action_space.n

print(actions)
