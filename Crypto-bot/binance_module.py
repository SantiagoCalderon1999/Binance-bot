#Binance dependencies
from binance.client import Client
from binance.enums import *

#project files
import config.binance_config 

# Processing libraries
import datetime
import pandas as pd

#Bring in Binance data
def get_recent_data(klines_interval, start_date, crypto_symbol):
    """
    :param klines_interval: Interval of klines
    :type klines_interval: str
    Available values klines intervals:
     1 minute - '1m',
     3 minutes - '3m',
     5 minutes - '5m',
     15 minutes - '15m',
     30 minutes - '30m',
     1 hour - '1h',
     2 hours - '2h',
     4 hours - '4h',
     6 hours - '6h',
     8 hours - '8h',
     12 hours - '12h',
     1 day -'1d',
     3 days - '3d',
     1 week - '1w',
     1 month -'1M'

     :param start_date: Start date for retrieving data
     :type start_date: str

     All formats available in https://dateparser.readthedocs.io/en/latest/
     """
    client = Client(config.binance_config.API_KEY, config.binance_config.API_SECRET, tld='com')
    symbolTicker = crypto_symbol + 'USDT'
    
    klines = client.get_historical_klines(symbolTicker, klines_interval, start_date + ' UTC')
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