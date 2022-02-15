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
from environment import CryptoTradingEnv

df = binance_module.get_recent_data()

# Create environment
training_steps = 2000
env = DummyVecEnv([lambda: CryptoTradingEnv(df, training_steps)])
model = A2C('MlpPolicy', env, verbose = 1)

#Train model
model.learn(total_timesteps = training_steps)
obs = env.reset()

#Test data
while True:
  action, _states = model.predict(obs)
  obs, rewards, done, info = env.step(action) 
  env.render() 
  if done:
    break
  
  
  

