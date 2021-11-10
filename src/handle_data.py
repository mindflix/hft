import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from utils import ensure_dir


def save_historical_klines(client, symbols, interval, start_time, limit=1000):
    """Gets klines for symbols.

        :param client: Client authentification
        :param symbols: required e.g NNB-0AD_BNB
        :param interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        :param limit:
        :param start_time:
        :param end_time:
        """

    for symbol in symbols:
        print(f'\n-> Gathering {symbol} data...')

        data = client.get_historical_klines(
            symbol=symbol, interval=interval, start_str=start_time, limit=limit)

        for line in data:
            del line[6:]

        cols = ["Time", 'Open', 'High', 'Low', 'Close', 'Volume']

        temp_df = pd.DataFrame(data, columns=cols)

        ensure_dir("data/{}".format(symbol))
        address = "data/{0}/{0}_{1}.csv".format(symbol, interval)
        temp_df.to_csv(address, index=False)

        print(f'-> Store {symbol} data to {address}')


def create_graph(symbol, interval):
    """Show a plotly graph for a  single symbol.

        :param symbols: required e.g NNB-0AD_BNB
        :param interval: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    """
    path = "data/{0}/{0}_{1}.csv".format(symbol, interval)
    stocks = pd.read_csv(path)
    date = []

    for t in stocks['Time']:
        date.append(datetime.fromtimestamp(t/1000))

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
