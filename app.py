from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit
from dotenv import load_dotenv
from threading import Lock
from binance_streamer import BinanceStreamer
import json
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret' 
app.config["TEMPLATES_AUTO_RELOAD"] = True

socketio = SocketIO(app, async_mode=None)


# Credentials
load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET")


thread_lock = Lock()
thread = None


crypto_list = ["BTCUSDT", "ETHUSDT", "XRPUSDT","LTCUSDT", "XMRUSDT", "BNBUSDT", "XLMUSDT",
               "ETHBTC", "XRPBTC","LTCBTC", "XMRBTC", "BNBBTC", "XLMBTC"]

streamer = BinanceStreamer(crypto=crypto_list)

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


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


if __name__ == '__main__':
    socketio.run(app,debug=True)
