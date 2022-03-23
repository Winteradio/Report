import gym
env = gym.make("FrozenLake-v1")

observation = env.reset()

for _ in range(1000):
    env.render()
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
