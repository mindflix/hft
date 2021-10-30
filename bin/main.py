from binance import ThreadedWebsocketManager
import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')


def main():

    symbol = 'BTCUSDT'

    twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=SECRET_KEY)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        symbol = msg["s"]
        price = msg["p"]
        quantity = msg["q"]
        

    twm.start_trade_socket(callback=handle_socket_message, symbol=symbol)

    twm.join()


if __name__ == "__main__":
    main()
