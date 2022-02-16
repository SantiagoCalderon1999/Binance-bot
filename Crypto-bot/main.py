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
import helpers

df = binance_module.get_recent_data()

training_percentage = 0.7
df_train, df_test = helpers.split_DataFrame(df, training_percentage)

# Create environments
training_steps = 20000
env_train = DummyVecEnv([lambda: CryptoTradingEnv(df_train, training_steps)])
env_test = DummyVecEnv([lambda: CryptoTradingEnv(df_test, training_steps)])

model = A2C('MlpPolicy', env_train, verbose = 1)

#Train model
model.learn(total_timesteps = training_steps)
obs = env_test.reset()

#Test data
while True:
  action, _states = model.predict(obs)
  obs, rewards, done, info = env_test.step(action) 
  env_test.render() 
  if done:
    break


  
  
  

