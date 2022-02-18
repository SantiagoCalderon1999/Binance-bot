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

klines_interval = '4h'
start_date = '365 days ago'
crypto_symbol = 'BTC'
df = binance_module.get_recent_data(klines_interval, start_date, crypto_symbol)

training_percentage = 0.7
df_train, df_test = helpers.split_DataFrame(df, training_percentage)

# Create environments
training_steps = 10000
env_train = DummyVecEnv([lambda: CryptoTradingEnv(df_train, training_steps)])
env_test = DummyVecEnv([lambda: CryptoTradingEnv(df_test, training_steps)])

models = []

models_quantity = 10
iteration_per_model = 10
#Train models
for i  in range(models_quantity):
  models.append(A2C('MlpPolicy', env_train, verbose = 1))
  models[i].learn(total_timesteps = training_steps)

#Test data
best_net_worth = 0
index_best_net_worth = 0
net_worth_accum = 0
average_net_worth = 0
internal = []
external = []
for i  in range(models_quantity):
  print(f'Model {i + 1}')
  net_worth_accum = 0
  internal =[]
  for j in range(iteration_per_model):
    print(f'Iteration {j + 1}')
    obs = env_test.reset()    
    while True:
      action, _states = models[i].predict(obs)
      obs, rewards, done, info = env_test.step(action) 
      if done:
        break

    final_net_worth = info[0].get('last_net_worth_normalized')
    internal.append(final_net_worth)
    net_worth_accum += final_net_worth
  external.append(internal)
  average_net_worth = net_worth_accum / iteration_per_model
  if (average_net_worth > best_net_worth):
    best_net_worth = average_net_worth
    index_best_net_worth = i

#Iterate best model
while True:
    action, _states = models[index_best_net_worth].predict(obs)
    obs, rewards, done, info = env_test.step(action) 
    env_test.render() 
    if done:
      break

print(f'Best net worth: {best_net_worth}')
print(f'Best model: # {index_best_net_worth + 1}')
  
  
  

