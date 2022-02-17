import random
import json
import gym
from gym import Env
from gym import spaces
import pandas as pd
import numpy as np
import plotting

#Fee is 0.1%
BINANCE_TRADING_FEE = 0.001 

INITIAL_ACCOUNT_BALANCE = 1000

class CryptoTradingEnv(Env):
   
    metadata = {'render.modes': ['human']}

    def __init__(self, df, training_steps):
        super(CryptoTradingEnv, self).__init__()
        self.training_steps = training_steps
        self.df = df
        
        # Action space vector has two values:
        #       First value determines the action: [0,1) -> buy, [1,2) -> sell, [2,3) -> hold 
        #       Second value is the amount of shares bought or sold
        self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)

        #Observation matrix includes: Open, High, Low, Close and volume of the last 5 steps
        self.observation_space = spaces.Box(low=0, high=1, shape=(5, 6), dtype=np.float16)

    def _get_observation(self):
        return np.array([
            self.df.loc[self.current_step: self.current_step + 5, 'Open'].values / self.df['Open'].max(),
            self.df.loc[self.current_step: self.current_step + 5, 'High'].values / self.df['High'].max(),
            self.df.loc[self.current_step: self.current_step + 5, 'Low'].values / self.df['Low'].max(),
            self.df.loc[self.current_step: self.current_step + 5, 'Close'].values / self.df['Close'].max(),
            self.df.loc[self.current_step: self.current_step + 5, 'Volume'].values / self.df['Volume'].max(),
        ])


    def _buy(self, current_price, amount):   
        #print("Buy")     
        amount_bought = self.static_money * amount

        self.fee = BINANCE_TRADING_FEE * amount_bought
        self.fee_acum += self.fee
        self.fee_tracking.append([self.df.loc[self.current_step, "Date"], self.fee_acum])
                   
        self.static_money -= amount_bought
        self.static_money -= self.fee

        self.crypto_held += amount_bought / current_price

        self.buy_indexes.append(self.current_step)

    def _sell(self, current_price, amount):
        amount_sold = self.crypto_held * amount * current_price
        
        self.fee = BINANCE_TRADING_FEE * amount_sold
        self.fee_acum += self.fee
        self.fee_tracking.append([self.df.loc[self.current_step, "Date"], self.fee_acum])
        
        self.static_money += amount_sold
        self.static_money -= self.fee

        self.crypto_held -= self.crypto_held * amount

        self.sell_indexes.append(self.current_step)

    def _hold(self):
        self.hold_indexes.append(self.current_step)

    def _perform_action(self, action):
        current_price =  self.df.loc[self.current_step, "Close"]

        action_type = action[0]
        self.last_action_value = action_type
        amount = action[1]
        
        #Buy if action_type is in the interval [0,1)
        if (action_type < 1  and amount > 0 and self.static_money > 0):
           self._buy(current_price, amount)

        #Sell if action_type is in the interval [1,2)
        elif (action_type < 2 and action_type >= 1 and self.crypto_held > 0 and amount > 0):
           self._sell(current_price, amount)

        #Hold if action_type is in the interval [2,3)
        else:
            self._hold()

        self.net_worth = self.static_money + self.crypto_held * current_price
        self.net_worth_array.append([self.df.loc[self.current_step, "Date"], self.net_worth])
        
    def _plot(self):
        plotting.plot_crypto_data_buy_sell(self.df, 
                                      self.buy_indexes_plot, 
                                      self.sell_indexes_plot, 
                                      self.hold_indexes_plot)
        plotting.plot_comparation_crypto_data(self.df_net_worth, "Net worth", self.df, "Crypto value")
        plotting.plot_simple_crypto_data(self.df_fee_tracking, "Fees")
    def step(self, action):
        self._perform_action(action)

        self.current_step += 1

        if self.current_step > len(self.df.loc[:, 'Open'].values) - 6:
            self.current_step = 0

        delay_modifier = (self.current_step / self.training_steps)

        reward = self.net_worth / INITIAL_ACCOUNT_BALANCE * delay_modifier

        obs = self._get_observation()
        if ((len(self.df) - 6) == self.current_step) | (self.net_worth <= 0):
            done = True
            self.buy_indexes_plot = self.buy_indexes
            self.sell_indexes_plot = self.sell_indexes
            self.hold_indexes_plot = self.hold_indexes
            self.df_net_worth = pd.DataFrame(self.net_worth_array,
                                             columns =['Date','Close'])
            self.df_fee_tracking = pd.DataFrame(self.fee_tracking,
                                                columns =['Date','Close'])    
            self._plot()                             
        else:
            done = False

        info = {'last_net_worth' : self.net_worth}
        
        return obs, reward, done, info

    def reset(self):
        # Reset the state of the environment to an initial state
        self.static_money = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.crypto_held = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0
        self.last_action_value = 0
        self.current_step = 0
        self.fee = 0
        self.fee_acum = 0
        self.buy_indexes = []
        self.sell_indexes = []
        self.hold_indexes = []
        self.buy_indexes_plot = []
        self.sell_indexes_plot = []
        self.hold_indexes_plot = []
        self.net_worth_array = []
        self.fee_tracking = []
        self.df_net_worth = pd.DataFrame()
        self.df_fee_tracking = pd.DataFrame()
        #Returns initial observation
        return self._get_observation()

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        profit = self.net_worth - INITIAL_ACCOUNT_BALANCE
        
      
        # After finishing the counter of steps restart to 0, that's where it is plotted
        if (self.current_step == 0):
            pass

    def compare_results(self):
        plotting.plot_comparation_crypto_data(self.df_net_worth)

            
        
        