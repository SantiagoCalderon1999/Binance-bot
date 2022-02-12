# Gym dependencies
import gym
import gym_anytrading

# Stable baselines
from stable_baselines.common.vec_env import dummy_vec_env
from stable_baselines import A2C

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
klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_15MINUTE, "1 hour ago UTC")
Periodos =len(klines)
df = pd.concat([pd.DataFrame([[datetime.datetime.fromtimestamp(float(klines[i][0])/1000),float(klines[i][1]),float(klines[i][2]),float(klines[i][3]),float(klines[i][4]),float(klines[i][5])]], columns=['Date','Open','High','Low','Close','Volume']) for i in range(Periodos)], ignore_index=True)

df.head()