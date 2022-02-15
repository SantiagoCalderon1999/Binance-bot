import matplotlib.pyplot as plt

def plot_crypto_data(df, buy_indexes, sell_indexes, hold_indexes):
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