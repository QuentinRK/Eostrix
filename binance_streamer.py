from binance import Client, ThreadedWebsocketManager

class BinanceStreamer:
    def __init__(self, crypto=[]):
        self.crypto = crypto
        self.price_change = False
        self.crypto_prices = {}
        self.manager = None

    def initManager(self, api_key, secret_key):
        self.manager = ThreadedWebsocketManager(api_key=api_key, api_secret=secret_key)
        self.manager.start()
    
    def startStream(self):
        streams = list(map(lambda x: x.lower() + "@aggTrade", self.crypto))
        self.manager.start_multiplex_socket(callback=self.handle_message, streams=streams)

    def stopStream(self):
        self.manager.stop()

    def handle_message(self, msg):
        length = len(msg["data"])
        symbol = msg["data"]["s"]
        current_price = msg["data"]["p"]
        self.msg = current_price

        if (symbol not in self.crypto_prices):
            self.crypto_prices[f"{symbol}"] = {"Price": current_price}
        else:
            last_price = self.crypto_prices[f"{symbol}"]["Price"]

            if (current_price != last_price):
                self.crypto_prices[f"{symbol}"]["Price"] = current_price
                self.price_change = True
            else:
                self.price_change = False
            
   

    def livePrices (self):
        return self.crypto_prices


if __name__== '__main__':
    BinanceStreamer()