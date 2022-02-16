import matplotlib.pyplot as plt

def plot_simple_crypto_data(df, name):
    plt.plot(df['Date'], 
            df['Close'], 
            label=name)
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.xticks(rotation=70)
    plt.legend(loc=0)
    plt.show()

def plot_comparation_crypto_data(df_1, name_1, df_2, name_2):
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
    plt.plot(df.iloc[hold_indexes]['Date'], 
            df.iloc[hold_indexes]['Close'], 
            '.', 
            markersize=10, 
            color='b')
    plt.ylabel('Close price')
    plt.xlabel('Date')
    plt.xticks(rotation=70)
    plt.legend(loc=0)
    plt.show()