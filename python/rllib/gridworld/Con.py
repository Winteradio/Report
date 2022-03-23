# -*- coding: utf-8 -*-
import gym,ray
import numpy as np

from gym.utils import seeding
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
from ray.tune.logger import pretty_print    

class MyEnv(gym.Env):
    NUM=1
    # possible positions
    LF_MIN = 1
    RT_MAX = 10
    
    '''
    {- - - - - - - - - -}
    위와 같이 10개의 자리를 지닌 칸으로 이루어진 맵
    >> LF_MIN : 제일 왼쪽은 위치상 1
    >> RT_MAX : 제일 오른쪽은 위치상 10
    '''

    # land on the GOAL position with MAX_STEPS steps
    MAX_STEPS = 10
   
    '''
    Goal 지점에 도달하기 위해서 최대의 Step(횟수)를 10번으로 지정
    '''
        # 사용하지 않는 것을 설정한다.

    # possible rewards
    '''
    보상 : (+)의 보상
    패널티 : (-)의 보상
        보상이 주어지는 경우를 어떻게 설정할 것인가?
            1.MAX_STEPS 의 반틈 정보만 이동하였을 때, 보상이 크게 주어진다.
                >> MAX_STEPS에 가까워져서 TRUE가 될 시, 패널티가 주어진다.
                >> REWARD_STEP = -count**2 && if count == MAX_STEPS : REWARD += -count**2

            2.한칸 이동할 때, 주어진 config에 맞춰서 이동할 시 높은 보상이 주어진다.
                >> config에 맞춰서 action을 진행할 시, 보상이 크게 주어진다.
                >> REWARD_CONFIG = abs(config - action)*3

            3.Goal 지점에 도달할 시, 가장 큰 보상이 주어진다.
                >> REWARD_GOAL = 100

            4.Left와 Right 양 끝에 도달할 시, 매우 큰 패널티가 주어진다.
                >> REWARD_AWAY = -50 * count **2
    '''

    error = 0.4
    
    '''
    만약에 Goal 지점의 위치가 5이고,
    현재 agents의 state가 4.95일시, Goal로 간주
            ''            4.80일시, No Goal로 간주
    '''

    def __init__(self,config):
        self.config = config

        self.action_space=gym.spaces.Box(-5.0,5.0,shape=(1,),dtype = np.float32)
        
        '''
        action은 왼쪽으로 이동하느냐 or 오른쪽으로 이동하느냐
            1. 왼쪽 이동
                >> (-) 방향으로 이동

            2. 오른쪽 이동
                >> (+) 방향으로 이동

            3. 연속적으로 이동한다. (-5,5) 사이에서 float의 형태로 주어지는 값으로 이동
        '''

        self.observation_space = gym.spaces.Box(self.LF_MIN,self.RT_MAX,shape=(1,),dtype=np.float32)
        
        '''
        observation space는 1,10사이의 값을 주어진다. 
            1. 시작점 : 왼쪽점 > 1 지점

            2. 끝점 : 으론점 > 10 지점
        '''
        
        self.reset()

    def reset(self):
        self.count = 0
        
        self.goal = np.array(self.observation_space.sample())
        self.position=np.array(self.observation_space.sample())
        self.reward = 0
        self.done = False
        self.info= {}
        self.state = self.position

        return self.state

    def step(self,action):
        try :
            assert self.action_space.contains(action)
        except AssertionError :
            print("Action 값이 Action Space 범위를 벗어났습니다. : ", action)
        
        self.count +=1
        self.position = self.state

        ## MOVE
        self.position += action
        self.reward = self.REWARD_STEP() + self.REWARD_CONFIG(action)
        ## Goal 여부 확인
        if abs(self.position[0]-self.goal[0]) < self.error :
            self.reward += self.REWARD_GOAL()
            self.done=True
        if self.position[0] < 1 or self.position[0] > 10:
            self.reward += self.REWARD_AWAY()

            if self.position[0] <1:
                self.position[0] =1

            elif self.position[0] > 10:
                self.position[0] = 10
            
        self.reward += self.REWARD_DIFF(self.position[0],self.goal[0])
        self.state=self.position

        try :
            assert self.observation_space.contains(self.state)
        except AssertionError :
            print("State 값이 Observation Space 범위를 벗어났습니다. :", self.state)

        return self.state,self.reward,self.done,self.info

    def close(self):
        pass

    def REWARD_STEP(self):
        REWARD = -self.count*0.1
        return float(REWARD)

    def REWARD_CONFIG(self,action):
        return -float(abs(abs(self.config) - abs(action)))*2
        
    def REWARD_GOAL(self):
        return 20

    def REWARD_AWAY(self):
        return -10
    
    def REWARD_DIFF(self,x,y):
        return -float(abs(x-y)*5)

def main():
    ray.init()
    register_env("my_env",lambda config : MyEnv(1.4))
    trainer = ppo.PPOTrainer(env="my_env")
    for i in range(50+1):
        result = trainer.train()
        print("진행중 {}".format(i))
        if i % 10 == 0 :
            checkpoint = trainer.save()
            print("checkpoint saved at ", checkpoint)

if __name__=="__main__":
    main()

