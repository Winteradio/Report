from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math,gym,ray
import time
import numpy as np

from gym.utils import seeding
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
from ray.tune.logger import pretty_print

import Con2

class Drawing:

    def __init__(self):
        ray.init()
        register_env("my_env", lambda config : Con2.MyEnv(config))
        config = ppo.DEFAULT_CONFIG.copy()
        config["num_workers"] = 0
        self.agent = ppo.PPOTrainer(config = config, env = "my_env")
        self.agent.restore("/home/tot4766/ray_results/PPO_my_env_2022-03-08_15-28-11t5klxsed/checkpoint_000701/checkpoint-701")
        self.env = Con2.MyEnv(1.4)
        self.obs = self.env.reset()
        self.episode_reward = 0
        self.done = False

    def update(self):
        self.obs,reward,self.done,self.info = self.env.step(self.agent.compute_action(self.obs))
        self.episode_reward +=reward
    
    def env_draw(self):
        glPointSize(20.0)
        glBegin(GL_POINTS)
        glColor3f(1.0,0.0,0.0)
        glVertex3f(self.env.goal[0],0,self.env.goal[0])

        if self.done == True :
            glColor3f(0.0,1.0,0)
        elif self.done == False:
            glColor3f(0.0,0.0,1.0)

        glVertex3f(self.obs[0],0,self.obs[1])
        glEnd()
        glFlush()
     
    def env_reset(self):
        if self.done == False:
            self.update()
        elif self.done == True:
            self.env.reset()
            self.done = False
    
    def baseline(self):
        for i in range(200):
            glLineWidth(2.0)
            glBegin(GL_LINES)
            glColor3f(0,0,0)
            glVertex3fv([-100+i,0,-100])
            glVertex3fv([-100+i,0,100])
            glVertex3fv([100,0,-100+i])
            glVertex3fv([-100,0,-100+i])
            glEnd()

        glLineWidth(2.0)
        glBegin(GL_LINES)    
        glColor3f(0,0,1)
        glVertex3fv([0,1,0])
        glVertex3fv([0,0,0])
        glEnd()

    def box(self,degree):
        glColor3f(0.5,0.0,0.2)
        glutSolidCube(1.0)
