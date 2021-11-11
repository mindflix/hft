import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import tqdm
from utils import ensure_dir, ensure_file, format_float_utc, format_utc_float


def get_dataset(client, symbols, interval, start_time, end_time=None, epochs=10):

    start_time = format_utc_float(start_time)
    if (end_time == None):
        end_time = datetime.now().timestamp()
    else:
        end_time = format_utc_float(end_time)

    increment = ((end_time - start_time) / epochs)

    data = []

    for epoch in tqdm(range(epochs * len(symbols)), desc="-> Gathering Data"):
        end_time = start_time + increment
        save_historical_klines(client, symbols, interval,
                               format_float_utc(start_time), format_float_utc(end_time))
        data.append([format_float_utc(start_time).split()[0],
                    format_float_utc(end_time).split()[0]])
        start_time = end_time
        epoch += 1

    df = pd.DataFrame(data, columns=["Start", "End"])

    print(df)

    ensure_file("data/datasets.json")
    if (os.stat("data/datasets.json").st_size != 0):
        df_temp = pd.read_json("data/datasets.json")
        df = pd.concat([df_temp, df], ignore_index=True)

    df.to_json("data/datasets.json", indent=4)

    print("-> Save dataset infos in data/datasets.json")

    return df


def save_historical_klines(client, symbols, interval, start_time, end_time=None, limit=1000):
    """Gets klines for symbols.

        :param client: Client authentification
        :param symbols: required e.g NNB-0AD_BNB
        :param interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        :param limit:
        :param start_time:
        :param end_time:
        """

    for symbol in symbols:

        data = client.get_historical_klines(
            symbol=symbol, interval=interval, start_str=start_time, end_str=end_time, limit=limit)

        for line in data:
            del line[6:]

        cols = ["Time", 'Open', 'High', 'Low', 'Close', 'Volume']

        temp_df = pd.DataFrame(data, columns=cols)

        ensure_dir("data/{}".format(symbol))
        if (end_time == None):
            end_time = datetime.utcnow()

        address = "data/{0}/{0}_{1}_({2}_{3}).csv".format(
            symbol, interval, str(start_time).split()[0], str(end_time).split()[0])
        temp_df.to_csv(address, index=False)


def create_graph(symbol, interval, start_time, end_time):
    """Show a plotly graph for a  single symbol.

        :param symbols: required e.g NNB-0AD_BNB
        :param interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    """
    path = "data/{0}/{0}_{1}_({2}_{3}).csv".format(
        symbol, interval, str(start_time).split()[0], str(end_time).split()[0])

    stocks = pd.read_csv(path)

    date = []

    for t in stocks['Time']:
        date.append(format_float_utc(t/1000))

    candlestick = go.Figure(data=[go.Candlestick(x=date,
                                                 open=stocks["Open"],
                                                 high=stocks["High"],
                                                 low=stocks["Low"],
                                                 close=stocks["Close"],
                                                 )])
    candlestick.update_layout(
        xaxis_rangeslider_visible=False, title=symbol)
    candlestick.update_xaxes(title_text="Date")
    candlestick.update_yaxes(title_text="Price", tickprefix="$")

    candlestick.show()

    print(stocks)
