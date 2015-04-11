

class Market:
    def __init__(self):
        self.next_id = 0
        self.state = "INACTIVE"
        self.stocks = {}
        self.trades = {}
        self.orders = {}

        # attempt connection
        self.socket = util.setup_connection()
        if self.socket is not None:
            pass

    def get_next_id(self):
        return ++self.next_id

    def __send_order(self, direction, symbol, price, size):
        util.send_json(self.socket, {
            'type': 'add',
            'order_id': self.get_next_id(),
            'symbol': symbol,
            'dir': direction,
            'price': price,
            'size': size
        })

    def __send_convert(self, direction, symbol, size):
        util.send_json(self.socket, {
            'type': 'convert',
            'order_id': self.get_next_id(),
            'symbol': symbol,
            'dir': direction,
            'size': size
        })

    def buy_order(self, symbol, price, size):
        self.__send_order('BUY', symbol, price, size)

    def sell_order(self, symbol, price, size):
        self.__send_order('SELL', symbol, price, size)

    def convert_buy_order(self, symbol, size):
        self.__send_convert('BUY', symbol, size)

    def convert_sell_order(self, symbol, size):
        self.__send__convert('SELL', symbol, size)

    def cancel_order(self, id):
        util.send_json(self.socket, {
            'type': 'cancel',
            'order_id': id
        })