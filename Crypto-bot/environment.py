import random
import json
import gym
from gym import Env
from gym import spaces
import pandas as pd
import numpy as np
import plotting

MAX_ACCOUNT_BALANCE = 2147483647
MAX_NUM_SHARES = 3000
MAX_SHARE_PRICE = 43000
MAX_OPEN_POSITIONS = 5
MAX_STEPS = 20000

#Fee is 0.1%
BINANCE_TRADING_FEE = 0.001 

INITIAL_ACCOUNT_BALANCE = 1000000

class CryptoTradingEnv(Env):
   
    metadata = {'render.modes': ['human']}

    def __init__(self, df, training_steps):
        super(CryptoTradingEnv, self).__init__()
        self.training_steps = training_steps
        self.df = df
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)
        self.buy_indexes_plot = []
        self.sell_indexes_plot = []
        self.hold_indexes_plot = []
        self.net_worth_array = []
        self.fee_tracking = []
        # Action space vector has two values:
        #       First value determines the action: [0,1) -> buy, [1,2) -> sell, [2,3) -> hold 
        #       Second value is the amount of shares bought or sold
        self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)

        #Observation matrix includes: Open, High, Low, Close and volume of the last 5 steps
        self.observation_space = spaces.Box(low=0, high=1, shape=(5, 6), dtype=np.float16)

    def _get_observation(self):
        return np.array([
            self.df.loc[self.current_step: self.current_step + 5, 'Open'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 5, 'High'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 5, 'Low'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 5, 'Close'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 5, 'Volume'].values / MAX_NUM_SHARES,
        ])


    def _buy(self, current_price, amount):        
        total_possible_shares = int(self.balance / current_price)
        shares_bought = int(total_possible_shares * amount)
        self.fee = BINANCE_TRADING_FEE * shares_bought * current_price
        self.fee_acum += self.fee
        self.fee_tracking.append([self.df.loc[self.current_step, "Date"], self.fee_acum])
        transaction_cost = shares_bought * current_price 
        
        self.balance -= transaction_cost
        self.balance -= self.fee
        self.shares_held += shares_bought
        self.buy_indexes.append(self.current_step)

    def _sell(self, current_price, amount):
        shares_sold = int(self.shares_held * amount)
        self.fee = BINANCE_TRADING_FEE * shares_sold * current_price
        self.fee_acum += self.fee
        self.fee_tracking.append([self.df.loc[self.current_step, "Date"], self.fee_acum])
        self.balance += shares_sold * current_price 
        self.balance -= self.fee

        self.shares_held -= shares_sold
        self.total_shares_sold += shares_sold
        self.total_sales_value += shares_sold * current_price
        self.sell_indexes.append(self.current_step)

    def _hold(self):
        self.hold_indexes.append(self.current_step)

    def _perform_action(self, action):
        current_price =  self.df.loc[self.current_step, "Close"]

        action_type = action[0]
        self.last_action_value = action_type
        amount = action[1]
        print(f'Action : {action_type}')
        
        #Buy if action_type is in the interval [0,1)
        if action_type < 1:
           self._buy(current_price, amount)

        #Sell if action_type is in the interval [1,2)
        elif action_type < 2:
           self._sell(current_price, amount)

        #Hold if action_type is in the interval [2,3)
        else:
            self._hold()

        self.net_worth = self.balance + self.shares_held * current_price
        self.net_worth_array.append([self.df.loc[self.current_step, "Date"], self.net_worth])
        

    def step(self, action):
        self._perform_action(action)

        self.current_step += 1

        if self.current_step > len(self.df.loc[:, 'Open'].values) - 6:
            self.current_step = 0

        delay_modifier = (self.current_step / self.training_steps)

        reward = self.net_worth * delay_modifier

        obs = self._get_observation()
        print(self.fee_acum)
        if ((len(self.df) - 6) == self.current_step) | (self.net_worth <= 0):
            done = True
            self.buy_indexes_plot = self.buy_indexes
            self.sell_indexes_plot = self.sell_indexes
            self.hold_indexes_plot = self.hold_indexes
            self.df_net_worth = pd.DataFrame(self.net_worth_array,
                                             columns =['Date','Close'])
            self.df_fee_tracking = pd.DataFrame(self.fee_tracking,
                                                columns =['Date','Close'])                                 
        else:
            done = False

        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.shares_held = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0
        self.last_action_value = 0
        self.current_step = 0
        self.fee = 0
        self.fee_acum = 0
        self.buy_indexes = []
        self.sell_indexes = []
        self.hold_indexes = []
        
        #Returns initial observation
        return self._get_observation()

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        profit = self.net_worth - INITIAL_ACCOUNT_BALANCE
        
      
        # After finishing the counter of steps restart to 0, that's where it is plotted
        if (self.current_step == 0):
            plotting.plot_crypto_data_buy_sell(self.df, 
                                      self.buy_indexes_plot, 
                                      self.sell_indexes_plot, 
                                      self.hold_indexes_plot)
            plotting.plot_comparation_crypto_data(self.df_net_worth, "Net worth", self.df, "Crypto value")
            plotting.plot_simple_crypto_data(self.df_fee_tracking, "Fees")
        else:
            print(f'Last action value: {self.last_action_value}')
            print(f'Step: {self.current_step}')
            print(f'Balance: {self.balance}')
            print(f'Shares held: {self.shares_held} (Total sold: {self.total_shares_sold})')
            print(f'Total sales value: {self.total_sales_value}')
            print(f'Net worth: {self.net_worth}')
            print(f'Profit: {profit}')
            print()

    def compare_results(self):
        plotting.plot_comparation_crypto_data(self.df_net_worth)

            
        
        