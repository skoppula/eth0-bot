import math
import market
import statistics
import time
import random
import sys
# Last trade,  self.stocks[symbol]['last trade'] approximate pnl
# Given a market state, output a fair value,

PENNY_SIZE = 1
TURNOVER = 1 #2 second turnover rate
MAX_NUM_ORDERS = 50 #50 active orders
FV_FUCKING_THRESHOLD = 0.3
POS_THRESHOLD = 10

def halfway_value(market, stock, info):
    # Halfway point between best bid (buy), best offer (sell) for stock
    # offer > bid
    best_bid = info['bid']
    best_offer = info['ask']
    return statistics.median([best_bid, best_offer])

def median_average(market, stock, info):
    temp_bid = [bids['price'] for bids in info['book_buy']]
    temp_offer = [offers['price'] for offers in info['book_sell']]
    median_bid = statistics.median(temp_bid) if len(temp_bid) != 0 else 0
    median_offer = statistics.median(temp_offer) if len(temp_offer) != 0 else 0
    return .5*(median_bid + median_offer)

def FV_attempt(market, stock, info):
    FV = halfway_value(market, stock, info)
    did_action = False
    for sells in info['book_sell']:
        #sells are [price, size]
        if sells[0] < FV(1-FV_FUCKING_THRESHOLD):
            market.buy_order(stock, sells[0], sells[1])
            did_action = True
    for buys in info['book_buy']:
        if buys[0] > FV(1+FV_FUCKING_THRESHOLD):
            if info['position'] > buys[1]:
                market.sell_order(stock, buys[0], buys[1])
                did_action = True
    return did_action

def penny(market, stock, info):
    if info['last_trade'] == 0:
        return
    penny_buy = info['bid'] + 1
    penny_sell = info['ask'] - 1

    if random.random() > 0.5 or market.stocks[stock]['position'] > POS_THRESHOLD:
        temp = [values['price'] for values in market.get_orders(stock).values() if values['dir'] == 'SELL']
        current_sell_order = min(temp) if len(temp) != 0 else sys.maxint
        if current_sell_order >= info['ask']:
            market.sell_order(stock, penny_sell, PENNY_SIZE)

    else:
        temp = [values['price'] for values in market.get_orders(stock).values() if values['dir'] == 'BUY']
        current_buy_order = max(temp) if len(temp) != 0 else 0
        if current_buy_order <= info['bid']:
            market.buy_order(stock, penny_buy, PENNY_SIZE)

    # avg = market.get_moving_avg(stock)
    #
    # print avg
    #
    # if avg is not None:
    #     if market.get_moving_avg(stock) > market.stocks[stock]['last_trade']:
    #         temp = [values['price'] for values in market.get_orders(stock).values() if values['dir'] == 'SELL']
    #         current_sell_order = min(temp) if len(temp) != 0 else sys.maxint
    #         if current_sell_order >= info['ask']:
    #             market.sell_order(stock, penny_sell, PENNY_SIZE)
    #     else:
    #         temp = [values['price'] for values in market.get_orders(stock).values() if values['dir'] == 'BUY']
    #         current_buy_order = max(temp) if len(temp) != 0 else 0
    #         if current_buy_order <= info['bid']:
    #             market.buy_order(stock, penny_buy, PENNY_SIZE)


def ETF_strategy(m):
    # Calculate the best buys and sells for a stock
    sell_margin = m.stocks["CORGE"]['bid']*10 - m.stocks["FOO"]['ask']*3 - m.stocks["BAR"]['ask']*8
    buy_margin = m.stocks["FOO"]['bid']*3 + m.stocks["BAR"]['bid']*8 - m.stocks["CORGE"]['ask']*10
    if sell_margin > 100:
        m.convert_buy_order("CORGE", m.stocks['bidsize'])
        m.sell_order("CORGE", m.stocks["CORGE"]['bid'], m.stocks["CORGE"]['bidsize'])
    if buy_margin > 100:
        # Convert CORGE to FOO/BAR and sell at bid price
        num_corge = m.stocks["CORGE"]['position']
        max_convert = 10*(math.floor(num_corge/10.0))
        m.convert_sell_order("CORGE", max_convert)
        m.sell_order("FOO", m.stocks["FOO"]['bid'], .3*max_convert)
        m.sell_order("BAR", m.stocks["BAR"]['bid'], .8*max_convert)
    return

def order_timeout(m):
    current_time = time.time()
    orders = m.orders
    for order, order_info in orders.items():
        if order_info['state'] != market.CANCELLING and current_time - order_info['timestamp'] > TURNOVER:
            m.cancel_order(order)

# USE THIS FUNCTION:
def next_action(m):
    # takes in a market, computes a fair value, outputs some action based on strategy
    order_timeout(m)

    for stock, info in sorted(m.stocks.items(), key=lambda x: random.random()):
        if m.num_orders < MAX_NUM_ORDERS:
            #did_action = FV_attempt(m, stock, info)
            #if not did_action:
            penny(m, stock, info)
                #ETF_strategy(m)
