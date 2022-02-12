# Gym dependencies
import gym
import gym_anytrading

# Stable baselines
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import A2C

# Processing libraries
import numpy as np
from matplotlib import pyplot as plt

#project files
import binance_module

df = binance_module.get_recent_data()

env = gym.make('stocks-v0', df=df, frame_bound=(10,200), window_size = 5)

state = env.reset()

while True:
    action = env.action_space.sample()
    n_state, reward, done, info = env.step(action)
    if done:
        print('info', info)
        break
plt.figure(figsize=(15,6))
plt.cla()
env.render_all()
plt.show()


#Build environment

env_maker = lambda: gym.make('stocks-v0', df=df, frame_bound=(10,100), window_size = 5)
env = DummyVecEnv([env_maker])

model = A2C('MlpPolicy', env, verbose = 1)
model.learn(total_timesteps=100000)


env = gym.make('stocks-v0', df=df, frame_bound=(80,110), window_size=5)
obs = env.reset()

while True:
    obs = obs[np.newaxis,...]
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    if done:
        print("info", info)
        break
plt.figure(figsize=(15,6))
plt.cla()
env.render_all()
plt.show()



