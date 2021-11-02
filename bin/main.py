from json.decoder import JSONDecodeError
from binance import ThreadedWebsocketManager
import os
import json
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
TRADES_JSON = "bin/trades.json"

trades_data = []


def load_data():
    with open(TRADES_JSON, "r") as json_file:
        try:
            old_trades = json.load(json_file)
            trades_data = old_trades
        except JSONDecodeError:
            pass


def write_data():
    with open(TRADES_JSON, "w") as json_file:
        json.dump(trades_data, json_file, indent=4)


def main():

    symbol = 'BTCUSDT'

    load_data()

    twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=SECRET_KEY)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        if (msg):
            trades_data.append(msg)
            write_data()

    twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)

    twm.join()


if __name__ == "__main__":
    main()
