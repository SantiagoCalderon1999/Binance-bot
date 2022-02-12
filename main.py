# Gym dependencies
import gym
import gym_anytrading

# Stable baselines
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import A2C

# Processing libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import datetime

#Binance dependencies
from binance.client import Client
from binance.enums import *

#external files
import config

#Bring in Binance data

client = Client(config.API_KEY, config.API_SECRET, tld='com')
symbolTicker = 'BTCUSDT'
klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_1HOUR, "50 day ago UTC")
Periodos =len(klines)
df = pd.concat([pd.DataFrame([[datetime.datetime.fromtimestamp(float(klines[i][0])/1000),
                float(klines[i][1]),
                float(klines[i][2]),
                float(klines[i][3]),
                float(klines[i][4]),
                float(klines[i][5])]], 
                columns=['Date','Open','High','Low','Close','Volume']) for i in range(Periodos)], 
                ignore_index=True)

df.set_index('Date', inplace=True)

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



