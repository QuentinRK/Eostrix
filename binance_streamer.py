from binance import ThreadedWebsocketManager

# This class requires an input of crypto currency pairs to run 
class BinanceStreamer:
    def __init__(self, crypto=[]):
        self.crypto = crypto
        self.crypto_prices = {}
        self.manager = None

    # Initalised the Websocket manager 
    def initManager(self, api_key, secret_key):
        self.manager = ThreadedWebsocketManager(api_key=api_key, api_secret=secret_key)
        self.manager.start()

    # Specify the types of streams and starts the connection 
    def startStream(self):
        aggTrades = list(map(lambda x: x.lower() + "@aggTrade", self.crypto))
        tickers = list(map(lambda x: x.lower() + "@ticker", self.crypto))
        self.manager.start_multiplex_socket(callback=self.aggTrade_handler, streams=aggTrades)
        self.manager.start_multiplex_socket(callback=self.ticker_handler, streams=tickers)

    def stopStream(self):
        self.manager.stop()

    """
        One of two message handlers that process the data received in the websocket connection  
        All prices are stored in the crypto_prices dictionary.
        It is only updated if there is a price change
    """
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


    """
        This handler process the price change percentage for the currency pairs.
        This data is also stored in the crypto_price dictionary 
    """
    def ticker_handler(self, msg):
        length = len(msg["data"])
        symbol = msg["data"]["s"]
        percent_change = msg["data"]["P"]
        self.msg = msg

        if (symbol not in self.crypto_prices) or ("price_change" not in self.crypto_prices[f"{symbol}"]):
            self.crypto_prices[f"{symbol}"] = {"price_change": percent_change}
        else:
            last_percent_change = self.crypto_prices[f"{symbol}"]["price_change"]

            if (percent_change != last_percent_change):
                percent_change = self.crypto_prices[f"{symbol}"]["price_change"] = percent_change
      

if __name__== '__main__':
    BinanceStreamer()