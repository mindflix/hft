from time import time
import pandas as pd
from binance import Client
import os
from dotenv import load_dotenv
from handle_data import save_historical_klines, create_graph
from utils import format_date_float, format_float_date, ensure_file


load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('SECRET_KEY')


def create_datasets(client, symbols, interval, start_time, end_time=None, epochs=10):

    start_time = format_date_float(start_time)
    if (end_time == None):
        end_time = time()
    else:
        end_time = format_date_float(end_time)

    increment = ((end_time - start_time) / epochs)

    data = []

    for epoch in range(epochs):
        end_time = start_time + increment
        data.append([format_float_date(start_time),
                    format_float_date(end_time)])
        start_time = end_time
        epoch + 1

    df_temp = pd.DataFrame(data, columns=["Start", "End"])

    ensure_file("data/datasets.json")
    if (os.stat("data/datasets.json").st_size != 0):
        df = pd.read_json("data/datasets.json")
        df_temp = pd.merge(df, df_temp)
    df_temp.to_json("data/datasets.json", indent=4)

    print(data)


def main():
    symbols = ['BTCUSDT']

    client = Client(API_KEY, API_SECRET)

    create_datasets(client, symbols, "1d", "10 Jun 2021")


if __name__ == "__main__":
    main()
