import requests
import pandas as pd
import os
from dotenv import load_dotenv
from binance import Client

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('SECRET_KEY')
SYMBOL = 'BTCUSDT'
INTERVAL = '1d'


client = Client(API_KEY, API_SECRET)

timestamp = client._get_earliest_valid_timestamp(SYMBOL, INTERVAL)

bars = client.get_historical_klines(SYMBOL, INTERVAL, timestamp, limit=1000)

for line in bars:
    del line[5:]

btc_df = pd.DataFrame(bars, columns=["date", "open", "high", "low", "close"])
btc_df.set_index("date", inplace=True)
print(btc_df.head())

# export DataFrame to csv
btc_df.to_csv("btc_bars.csv")
