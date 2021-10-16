import os
import pprint
import json
from dotenv import load_dotenv
import websocket


load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kstick_1m"

closes = []


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("### opened ###")


def on_message(ws, message):
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']


def main():
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()


if __name__ == "__main__":
    main()
