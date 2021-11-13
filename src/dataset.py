import pandas as pd
import plotly.graph_objects as go
from tqdm import tqdm
import sqlalchemy as sal
from utils import get_fromtimestamp_ms, get_timestamp_ms


class DatasetDownloader:
    """Class that extract and manage the datasets for Inputs of Neural Network

        :param client: Client authentification
        """

    def __init__(self, client):
        self.client = client
        self.db = sal.create_engine("mysql://root:poplpo@localhost/datasets")

    def create_dataset(self, symbol, timeframe, start, end=None, epochs=1):
        """Create a dataset and save it to SQL db.

            :param symbol: required e.g BTCUSDT
            :param timeframe: required 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
            :param start: required "2021-10-10 00:00:00"
            :param end: "2021-11-10 00:00:00"
            :param epochs: integrer
            """
        start, end = get_timestamp_ms(start, end)
        dataset_infos = []
        diff = ((end - start) / epochs)
        for epoch in tqdm(range(epochs), desc="-> Gathering Data for {}".format(symbol)):
            end = start + diff
            dataset_infos.append([symbol, timeframe, start, end])
            self.__fetch_klines(symbol, timeframe, start, end)
            start = end
            epoch += 1

        df_dataset_infos = pd.DataFrame(
            dataset_infos, columns=["symbol", "timeframe", "start", "end"])
        df_dataset_infos.to_sql(
            "infos", self.db, if_exists="append", index=False)
        print(f"-> Save {symbol} ({timeframe}) dataset in SQL")

    def __fetch_klines(self, symbol, timeframe, start, end=None, limit=5000):
        """Fetch klines from Binance API.

            :param symbol: required e.g BTCUSDT
            :param timeframe: required 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
            :param start: required timestamp in ms
            :param end: timestamp in ms
            """

        data = self.client.get_klines(
            symbol=symbol, interval=timeframe, startTime=int(start), endTime=int(end), limit=limit)

        for line in data:
            del line[6:]

        cols = ['time', 'open', 'high', 'low', 'close', 'volume']

        df = pd.DataFrame(data, columns=cols)
        df.to_sql(symbol + "_" + timeframe, self.db,
                  if_exists="append", index=False)

    def get_graph(self, symbol):
        """Show a plotly graph for a  single symbol.

            :param symbols: required e.g NNB-0AD_BNB
            :param timeframe: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        """

        stocks = pd.read_sql(symbol, self.db)

        t_list = []

        for t in stocks['time']:

            t_list.append(get_fromtimestamp_ms(t))

        candlestick = go.Figure(data=[go.Candlestick(x=t_list,
                                                     open=stocks["open"],
                                                     high=stocks["high"],
                                                     low=stocks["low"],
                                                     close=stocks["close"],
                                                     )])
        candlestick.update_layout(
            xaxis_rangeslider_visible=False, title=symbol)
        candlestick.update_xaxes(title_text="Date")
        candlestick.update_yaxes(title_text="Price", tickprefix="$")
        candlestick.show()

        print(stocks)
