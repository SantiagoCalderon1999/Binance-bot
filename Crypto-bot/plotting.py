import matplotlib.pyplot as plt
import numpy as np

def plot_simple_crypto_data(df, name):
    plt.clf()
    plt.plot(df['Date'], 
            df['Close'], 
            label=name)
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.xticks(rotation=70)
    plt.legend(loc=0)
    plt.show()

def plot_comparison_crypto_data(df_1, name_1, df_2, name_2):
    plt.clf()
    plt.plot(df_1['Date'], 
            df_1['Close']/df_1['Close'][0], 
            label=name_1)
    plt.plot(df_2['Date'], 
            df_2['Close']/df_2['Close'][0], 
            label=name_2)
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.xticks(rotation=70)
    plt.legend(loc=0)
    plt.show()

def plot_crypto_data_buy_sell(df, buy_indexes, sell_indexes, hold_indexes):
    plt.clf()
    plt.plot(df['Date'], 
            df['Close'], 
            label='Close price')
    plt.plot(df.iloc[buy_indexes]['Date'], 
             df.iloc[buy_indexes]['Close'], 
            '^', 
            markersize=10, 
            color='g')
    plt.plot(df.iloc[sell_indexes]['Date'], 
             df.iloc[sell_indexes]['Close'], 
            'v', 
            markersize=10, 
            color='r')
    plt.ylabel('Close price')
    plt.xlabel('Date')
    plt.xticks(rotation=70)
    plt.legend(loc=0)
    plt.show()

def plot_comparison(array):
    plt.clf()
    model_quantity = len(array)
    iterations_per_model = len(array[0])
    index_array = np.linspace(1,iterations_per_model, iterations_per_model)
    for i in range(model_quantity):
            name = "Model " + str(i + 1)
            plt.plot(index_array, 
                     array[i],
                     label = name)
    plt.ylabel('Value')
    plt.xlabel('Index')
    plt.legend(loc=0)
    plt.show()
        


