from time import time, ctime
from binance import Client
import os
from dotenv import load_dotenv
from handle_data import save_historical_klines, create_graph


load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('SECRET_KEY')


def main():
    symbols = ['BTCUSDT']

    client = Client(API_KEY, API_SECRET)

    save_historical_klines(client, symbols, "30m", "1 Nov 2021")

    create_graph(symbols[0], "30m")


if __name__ == "__main__":
    main()
