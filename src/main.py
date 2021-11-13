import os
from dotenv import load_dotenv
from binance import Client
from dataset import DatasetDownloader


load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('SECRET_KEY')


def main():
    symbol = 'BTCUSDT'

    client = Client(API_KEY, API_SECRET)
    dataset = DatasetDownloader(client)

    dataset.create_dataset(symbol, "1h", "2021-10-01", epochs=10)


if __name__ == "__main__":
    main()
