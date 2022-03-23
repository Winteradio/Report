import gym,ray
import numpy as np

from gym.utils import seeding
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
from ray.tune.logger import pretty_print

class MyEnv(gym.Env):
    # possible actions
    MOVE_LF = 0
    MOVE_RT = 1

    # possible positions
    LF_MIN = 1
    RT_MAX = 10

    # land on the GOAL position with MAX_STEPS steps
    MAX_STEPS = 10
    # possible rewards
    REWARD_AWAY = -2
    REWARD_STEP = -1
    REWARD_GOAL = MAX_STEPS

    metadata = {
            "render.moes" : ["human"]
            } 
    # >> metatdata가 존재하는 이유는 뭐지??

    def __init__(self,config):
        # the actions space ranges [0,1] where:
        #   액션은 0과 1 중 하나의 값으으로 왼쪽 혹은 오른쪽으로 이동
        # "0" move left
        # "1" move right

        self.action_space=gym.spaces.Discrete(2)
        # 왜냐하면 0과 1, 두가지의 액션밖에 없기 때문

        # NB : Ray throws exceptions for any '0' value Discrete
        # observations so we'll make position a 1's based value

        self.observation_space = gym.spaces.Discrete(self.RT_MAX+1)
        print(self.observation_space.n)
        # 왜 10이 아니고 11인가?
        # 0 ~ 10까지면 11개여서 RT_MAX +1이 아닐까?

        # possible positions to chose on 'reset()'
        self.goal = int ((self.LF_MIN + self.RT_MAX -1)/2)

        self.init_positions = list(range(self.LF_MIN,self.RT_MAX+1))
        self.init_positions.remove(self.goal)
        # init_positions : 초기 위치를 
        # 왜 초기 위치 리스트에서 골 지점을 제거할까?
        #   도착 지점에서는 출발하면 안되기때문이다.

        # NB : change to guarantee the sequence of pseudorandom numbers
        # ( e.g., for dubugging)
        self.seed()
        self.reset()

    def reset(self):
        self.position = self.np_random.choice(self.init_positions)
        self.count = 0

        # for this environment, state is simply the positions
        self.state = self.position
        self.reward = 0
        self.done = False
        self.info= {}

        return self.state

    def step(self,action):
        if self.done:
            print("EPISODE DONE!!!!")
        elif self.count == self.MAX_STEPS:
            self.done=True;

        else : 
            assert self.action_space.contains(action)
            self.count +=1

            if action == self.MOVE_LF:
                if self.position == self.LF_MIN :
                    self.reward = self.REWARD_AWAY
                else :
                    self.position -=1
                    

                    if self.position ==self.goal :
                        # on goal now
                        self.reward = self.REWARD_GOAL
                        self.done = 1

                    elif self.position > self.goal:
                        # moving away from GOAL
                        self.reward = self.REWARD_AWAY

                    else :
                        # moving toward GOAL
                        self.reward = self.REWARD_STEP

            elif action == self.MOVE_RT :
                if self.position == self.RT_MAX :
                    #invalid
                    self.reward = self.REWARD_AWAY

                else :
                    self.position +=1

                    if self.position == self.goal:
                        # on goal now
                        self.reward = self.REWARD_GOAL
                        self.done = 1

                    elif self.position > self.goal :
                        # moving away from GOAL
                        self.reward = self.REWARD_AWAY

                    else : 
                        # moving toward GOAL
                        self.reward = self.REWARD_STEP
        try :
            assert self.observation_space.contains(self.state)
        except AssertionError :
            print("INVALID STATE", self.state)

        self.state = self.position            
        self.render(action)
        return [self.state,self.reward,self.done,self.info]

    
    def render(self,action):
        if self.state != None:
            Ren = "{----------}"
            lst = [] 
            for i in range(len(Ren)):
                if i == self.state+1 :
                    lst.append("@")
                elif i == self.goal+1 :
                    lst.append("G")
                elif i == 0 :
                    lst.append("{")
                elif i == len(Ren)-1 :
                    lst.append("}")
                else :
                    lst.append("-")
            print(lst,"\n")
            print("Reward :",self.reward,"\n")
            
            if action ==0 :
                print("Action : Left \n")
            elif action ==1 :
                print("Action : Right \n")

    def seed(self,seed=None):
        self.np_random, seed= seeding.np_random(seed)
        return [seed]

    def close(self):
        pass

def main():
    ray.init()
    register_env("my_env",lambda config : MyEnv(config))
    trainer = ppo.PPOTrainer(env="my_env")
    for i in range(100):
        result = trainer.train()
        if i % 10 == 0 :
            checkpoint = trainer.save()
            print("checkpoint saved at ", checkpoint)

if __name__=="__main__":
    main()

