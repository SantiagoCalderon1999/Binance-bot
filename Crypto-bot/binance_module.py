#Binance dependencies
from binance.client import Client
from binance.enums import *

#project files
import config.binance_config as c

# Processing libraries
import datetime
import pandas as pd

#Bring in Binance data
def get_recent_data():
    client = Client(c.API_KEY, c.API_SECRET, tld='com')
    symbolTicker = 'BTCUSDT'
    klines = client.get_historical_klines(symbolTicker, Client.KLINE_INTERVAL_1HOUR, "50 day ago UTC")
    periods =len(klines)
    df = pd.concat([pd.DataFrame([[datetime.datetime.fromtimestamp(float(klines[i][0])/1000),
                    float(klines[i][1]),
                    float(klines[i][2]),
                    float(klines[i][3]),
                    float(klines[i][4]),
                    float(klines[i][5])]], 
                    columns=['Date','Open','High','Low','Close','Volume']) for i in range(periods)], 
                    ignore_index=True)

    return df