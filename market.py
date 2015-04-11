import sys
import util
import time

INACTIVE = 'INACTIVE'
OPEN = 'OPEN'
CLOSED = 'CLOSED'

PENDING = 'PENDING'
ACK = 'ACK'
PARTIALLY_FILLED = 'PARTIALLY_FILLED'
CANCELLING = 'CANCELLING'

BUY = 'BUY'
SELL = 'SELL'


class Market:
    def __init__(self):
        self.next_id = 0
        self.state = INACTIVE
        self.stocks = {}
        self.trades = {}
        self.orders = {}
        self.cash = 0
        self.num_orders = 0

        # attempt connection
        self.socket, self.infile = util.setup_connection()
        if self.socket is not None:
            start_state = util.send_hello(self.socket, self.infile)
            if start_state is not None and start_state['type'] == 'hello':
                self.cash = start_state['cash']
                self.stocks = {
                    stock['symbol']: {
                        'book_buy': [],
                        'book_sell': [],
                        'bid': 0,
                        'ask': 0,
                        'position': stock['position'],
                        'last_trade': 0,
                    }
                    for stock in start_state['symbols']
                }

                self.trades = {
                    stock['symbol']: [] for stock in start_state['symbols']
                }

                if start_state['market_open']:
                    self.state = OPEN
                else:
                    self.state = CLOSED

    def get_next_id(self):
        self.next_id = self.next_id + 1
        return self.next_id

    def __send_order(self, direction, symbol, price, size):
        order_id = self.get_next_id()
        order = {
            'state': PENDING,
            'symbol': symbol,
            'dir': direction,
            'price': price,
            'size': size,
            'timestamp': time.time()
        }
        self.orders[order_id] = order

        print 'ORDER #' + str(order_id) + ': \t' + str(direction) + '\t' \
            + str(symbol) + '\t' + str(price) + '\t' + str(size) + '\n'

        util.send_json(self.socket, {
            'type': 'add',
            'order_id': order_id,
            'symbol': symbol,
            'dir': direction,
            'price': price,
            'size': size
        })

        self.num_orders = self.num_orders + 1

    def __send_convert(self, direction, symbol, size):
        util.send_json(self.socket, {
            'type': 'convert',
            'order_id': self.get_next_id(),
            'symbol': symbol,
            'dir': direction,
            'size': size
        })

    def buy_order(self, symbol, price, size):
        self.__send_order(BUY, symbol, price, size)

    def sell_order(self, symbol, price, size):
        self.__send_order(SELL, symbol, price, size)

    def convert_buy_order(self, symbol, size):
        self.__send_convert(BUY, symbol, size)

    def convert_sell_order(self, symbol, size):
        self.__send_convert(SELL, symbol, size)

    def cancel_order(self, order_id):
        self.orders[order_id]['state'] = CANCELLING
        util.send_json(self.socket, {
            'type': 'cancel',
            'order_id': order_id
        })
        self.num_orders = max(self.num_orders - 1, 0)

    def __str__(self):
        return "Market:\n\t" + str(self.stocks) + "\n\t" + str(self.trades) \
            + "\n\t" + str(self.orders) + '\n'

    def get_orders(self, symbol):
        return {
            k: v
            for k, v in self.orders.items() if v['symbol'] == symbol
        }

    def approx_pnl(self):
        return reduce(
            lambda pnl, stock: stock['last_trade'] * stock['position'] + pnl,
            self.stocks.values(),
            self.cash
        )

    def update(self):
        msg = util.get_message(self.infile)

        if msg['type'] == 'book':
            self.stocks[msg['symbol']]['book_buy'] = msg['buy']
            self.stocks[msg['symbol']]['book_sell'] = msg['sell']

            self.stocks[msg['symbol']]['bid'] = reduce(
                lambda bid, x: max(bid, x[0]), msg['buy'], 0
            )
            self.stocks[msg['symbol']]['ask'] = reduce(
                lambda ask, x: min(ask, x[0]), msg['sell'], sys.maxint
            )

        elif msg['type'] == 'trade':
            self.trades[msg['symbol']].append({
                'price': msg['price'],
                'size': msg['size']
            })
            self.stocks[msg['symbol']]['last_trade'] = msg['price']
            print "PNL:" + str(self.approx_pnl()) + "\tCASH:" + str(self.cash) + \
                "\tFOO:" + str(self.stocks['FOO']['position']) + \
                "\tBAR:" + str(self.stocks['BAR']['position']) + \
                "\tBAZ:" + str(self.stocks['BAZ']['position']) + \
                "\tQUUX:" + str(self.stocks['QUUX']['position']) + \
                "\tCORGE:" + str(self.stocks['CORGE']['position']) + "\n"

        elif msg['type'] == 'ack':
            self.orders[msg['order_id']]['state'] = ACK

        elif msg['type'] == 'fill':
            print 'FILLED #' + str(msg['order_id']) + ': \t' + str(msg['dir']) \
                + '\t' + msg['symbol'] + '\t' + str(msg['price']) + '\t' \
                + str(msg['size']) + '\n'
            self.orders[msg['order_id']]['state'] = PARTIALLY_FILLED
            self.orders[msg['order_id']]['size'] = \
                self.orders[msg['order_id']]['size'] - msg['size']

            # update position and cash
            sign = 1 if msg['dir'] == BUY else -1
            self.stocks[msg['symbol']]['position'] += msg['size'] * sign
            self.cash = self.cash + msg['size'] * msg['price'] * (-sign)

        elif msg['type'] == 'out' or msg['type'] == 'reject':
            if 'order_id' in self.orders:
                del self.orders[msg['order_id']]
                self.num_orders = max(self.num_orders - 1, 0)
