import gym, ray
import numpy as np
from ray.rllib.agents import ppo
from ray.tune.registry import register_env
from ray.tune.logger import pretty_print

class MyEnv(gym.Env):

    def __init__(self, config=None) :
        if config is None :
            config = ENV_CONFIG
        super().__init__()
        self.environment_config=config

        self.action_space =gym.spaces.Discrete(3)
        self.observation_space =gym.spaces.Discrete(6)
        
        ''' 초기 위치 '''
        self.x = 0


    '''
    def decoding(self, encoding):
        list = []
        list.append(encoding %4)
        encoding -= encoding % 4
        list.append(encoding //4)

        return reversed(list)
    '''

    def reset(self) :
        self.x=0
        return self.x
        
    def step(self,action) :
        
        '''
        if action == 0:
            self.move_left()
        elif action == 1:
            self.move_right()
        '''
        if action ==0 : 
            self.move_up()
        elif action ==1 :
            self.move_down()
        elif action ==2 :
            self.move_rest()
        
        Reward = - 1

        done = self.is_done()

        return self.x , Reward, done
    
    def move_left(self):
        if self.y==0:
            pass
        else :
            self.y -= 1

    def move_right(self):
        if self.y==3 :
            pass
        else :
            self.y +=1

    def move_up(self):
        if self.x==0 :
            pass
        else :
            self. x -=1

    def move_down(self):
        if self.x ==3 :
            pass
        else :
            self. x +=1

    def move_rest(self):
        return self.x

    def is_done(self):
        if self.x==5:
            return True
        else :
            return False

def main():
    ray.init()
    register_env("my_env", lambda config : MyEnv(config))
    agent = ppo.PPOTrainer(env = "my_env")
    
    for i in range(1000):
        result = agent.train()
        print(pretty_print(result))
        if i %50 == 0 :
            checkpoint = agent.save()
            print("checkpoint saved at ", checkpoint)

if __name__ == '__main__':
    main()
