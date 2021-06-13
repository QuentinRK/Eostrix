from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit
from dotenv import load_dotenv
from threading import Lock
from binance_streamer import BinanceStreamer
from datetime import datetime
from os.path import exists
import json
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ["SECRET"]

socketio = SocketIO(app, async_mode=None)

# Credentials
load_dotenv(".env")
API_KEY = os.environ["API_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]


thread_lock = Lock()
thread = None

# Currency Pairs
crypto_list = ["BTCUSDT", "ETHUSDT", "XRPUSDT","LTCUSDT", "XMRUSDT", "BNBUSDT", "XLMUSDT",
               "ETHBTC", "XRPBTC","LTCBTC", "XMRBTC", "BNBBTC", "XLMBTC"]

streamer = BinanceStreamer(crypto=crypto_list)

"""
    Connects to the binance api through the BinanceStreamer class 
    Every second this thread emits this data to the client side 
""" 

def background_thread():
    streamer.initManager(API_KEY, SECRET_KEY)
    streamer.startStream()
    dictionary = streamer.crypto_prices
    while True:
        if (dictionary != {}) and streamer.price_change:
            socketio.emit('my_response', {'data': dictionary})
            time.sleep(1)

@app.route("/")
def index():
    return render_template("index.html", crypto=crypto_list, async_mode=socketio.async_mode)

@socketio.on('client_connected')
def message(data):
    print("Client:" + data['data'])


"""
    Every 24hours the update on the price change is logged to a txt file 
"""
@socketio.on('ticker_update')
def message(data):
    price_data = data['percentage']
    symbols_data = data['crypto']

    if price_data != []:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        price_change = list((str(symbols_data[i]) + ':' + str(price_data[i])) for i in range(len(symbols_data)))

        price_change = str(price_change)

        if (exists("log.txt")):
            with open("log.txt", 'a') as f:
                f.write(dt_string + ": " + price_change + "\n")
        else:
            file = open("log.txt", "x")
            file.write(dt_string + ": " + price_change + "\n")
            file.close()


# Runs the background thread that has a websocket connection to the binance API
@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


if __name__ == '__main__':
    socketio.run(app,debug=True)
