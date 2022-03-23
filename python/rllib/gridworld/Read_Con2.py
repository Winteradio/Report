# -*- coding: utf-8 -*-  
import gym,ray
import numpy as np
import time

from gym.utils import seeding
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
from ray.tune.logger import pretty_print

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import Con2

class Draw:
    def __init__(self):
        ray.init()
        register_env("my_env", lambda config: Con2.MyEnv(config))
        config = ppo.DEFAULT_CONFIG.copy()
        config["num_workers"]=0
        self.agent = ppo.PPOTrainer(config=config, env = "my_env")
        self.agent.restore("/home/tot4766/ray_results/PPO_my_env_2022-03-04_14-41-399hciuph_/checkpoint_000101/checkpoint-101")
        self.env=Con2.MyEnv(1.4)
        self.obs=self.env.reset()
        self.episode_reward = 0
        self.done=False


    def MyDisplay(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPointSize(30.0)
        glBegin(GL_POINTS)
        glColor3f(1.0,0,0)
        glVertex2f(self.Change(self.env.goal[0]),self.Change(self.env.goal[1]))
        if self.done == True:
            glColor3f(0.0,1.0,0)
        elif self.done == False:
            glColor3f(0.0,0.0,1.0)
        glVertex2f(self.Change(self.obs[0]),self.Change(self.obs[1]))
        glEnd()
        glFlush()

    def MyTimer(self,time):
        if self.done == False:
            self.update()
        elif self.done == True:
            self.env.reset()
            self.done = False
            self.episode_reward = 0
        glutPostRedisplay()
        glutTimerFunc(100,self.MyTimer,1)
    
    def main(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB)
        glutInitWindowSize(300,300)
        glutInitWindowPosition(0,0)
        glutCreateWindow("1-Coordinate Bar Learning")

        glutDisplayFunc(self.MyDisplay)
        glutTimerFunc(0,self.MyTimer,1)

        glutMainLoop()

    def update(self):
        self.obs,reward,self.done,info =self.env.step(self.agent.compute_action(self.obs))
        self.episode_reward +=reward
        print("REWARD : ",self.episode_reward)
    
    def Change(self,x):
        return float(x-5)/6
if __name__=="__main__":
    Start = Draw()
    Start.main()
