# -*- coding: utf-8 -*-
import gym,ray,math
import numpy as np

from gym.utils import seeding
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
from ray.tune.logger import pretty_print    

class MyEnv(gym.Env):
    MAX_NUM = 200
    # possible positions
    LF_MIN = -1e20
    RT_MAX = 1e20
    
    '''
    {- - - - - - - - - -}
    위와 같이 10개의 자리를 지닌 칸으로 이루어진 맵
    >> LF_MIN : 제일 왼쪽은 위치상 1
    >> RT_MAX : 제일 오른쪽은 위치상 10
    '''

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
        self.action_space=gym.spaces.Box(-1,1,shape=(2,),dtype = np.float32)
        
        '''
        action은 왼쪽으로 이동하느냐 or 오른쪽으로 이동하느냐
            1. 왼쪽 이동
                >> (-) 방향으로 이동

            2. 오른쪽 이동
                >> (+) 방향으로 이동

            3. 연속적으로 이동한다. (-5,5) 사이에서 float의 형태로 주어지는 값으로 이동
        '''

        self.observation_space = gym.spaces.Box(self.LF_MIN,self.RT_MAX,shape=(2,),dtype=np.float32) 
        '''
        observation space는 1,10사이의 값을 주어진다. 
            1. 시작점 : 왼쪽점 > 1 지점

            2. 끝점 : 으론점 > 10 지점
        '''
        self.New_Dis = 0
        self.Old_Dis = 0
        self.Scale = 0.2
        self.reset()

    def reset(self):
        self.count = 0
        
        self.goal = np.random.rand(2)*4
        self.position=np.random.rand(2)*4
        self.reward = 0
        self.Count = 0
        self.done = False
        self.MAX = False
        self.info= {}
        self.state = self.position

        return self.state

    def step(self,action):
        self.position = self.state
        
        if (self.Count >= self.MAX_NUM):
            self.done = True
            self.MAX = True
        else :

            ## MOVE
            move = np.tanh(action) * self.Scale
            self.position +=move
        
            ## Goal 여부 확인
            D_X = abs(self.position[0] - self.goal[0])
            D_Y = abs(self.position[1] - self.goal[1])
            self.Old_Dis = self.New_Dis
            self.New_Dis = math.sqrt(pow(D_X,2)+pow(D_Y,2))
        
            if self.New_Dis < self.error :
                self.reward += self.REWARD_GOAL()
                self.done=True

            self.state= self.position
        
            self.reward += self.REWARD_DIFF()

            self.Count +=1

        return self.state,self.reward,self.done,self.info

    def close(self):
        pass
   
    def REWARD_GOAL(self):
        return 100

    def REWARD_DIFF(self):
        return  -self.New_Dis*0.5

def main():
    ray.init()
    config = ppo.DEFAULT_CONFIG.copy()
    config["clip_param"] = 1.0
    config["vf_clip_param"] = 50000
    config["train_batch_size"] = 4000
    config["rollout_fragment_length"] = 200
    register_env("my_env",lambda config : MyEnv(1.4))
    trainer = ppo.PPOTrainer(config = config, env="my_env")
   
    for i in range(1000+1):
        result = trainer.train()
        print("{} 번째 진행 중".format(i+1))
        if i % 100 == 0 :
            checkpoint = trainer.save()
            print("checkpoint saved at ", checkpoint)

if __name__=="__main__":
    main()

