import os
from dotenv import load_dotenv
from binance import Client
from dataset import get_dataset


load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('SECRET_KEY')


def main():
    symbols = ['BTCUSDT']

    client = Client(API_KEY, API_SECRET)

    data = get_dataset(client, symbols, "1h", "2021-07-11")


if __name__ == "__main__":
    main()
