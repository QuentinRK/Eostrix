from binance import Client, ThreadedWebsocketManager

class BinanceStreamer:
    def __init__(self, crypto=[]):
        self.crypto = crypto
        self.price_change = False
        self.crypto_prices = {}
        self.msg = None
        self.manager = None

    def initManager(self, api_key, secret_key):
        self.manager = ThreadedWebsocketManager(api_key=api_key, api_secret=secret_key)
        self.manager.start()
    
    def startStream(self):
        aggTrades = list(map(lambda x: x.lower() + "@aggTrade", self.crypto))
        tickers = list(map(lambda x: x.lower() + "@ticker", self.crypto))
        self.manager.start_multiplex_socket(callback=self.aggTrade_handler, streams=aggTrades)
        self.manager.start_multiplex_socket(callback=self.ticker_handler, streams=tickers)

    def stopStream(self):
        self.manager.stop()

    def aggTrade_handler(self, msg):
        length = len(msg["data"])
        symbol = msg["data"]["s"]
        current_price = msg["data"]["p"]
        self.msg = msg

        if (symbol not in self.crypto_prices) or ("price" not in self.crypto_prices[f"{symbol}"]):
            self.crypto_prices[f"{symbol}"] = {"price": current_price}
        else:
            last_price = self.crypto_prices[f"{symbol}"]["price"]

            if (current_price != last_price):
                self.crypto_prices[f"{symbol}"]["price"] = current_price
                self.price_change = True
            else:
                self.price_change = False

    def ticker_handler(self, msg):
        length = len(msg["data"])
        symbol = msg["data"]["s"]
        percent_change = msg["data"]["P"]
        self.msg = msg

        if (symbol not in self.crypto_prices):
            self.crypto_prices[f"{symbol}"] = {"price_change": percent_change}
        else:
            percent_change = self.crypto_prices[f"{symbol}"]["price_change"] = percent_change
      

if __name__== '__main__':
    BinanceStreamer()