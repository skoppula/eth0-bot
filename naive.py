import market
import statistics
import time
# Last trade,  self.stocks[symbol]['last trade'] approximate pnl
# Given a market state, output a fair value, 

turnover = 1 #1 second turnover rate
num_orders = 50 #50 active orders

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
        if sells[0] < FV:
            market.buy_order(stock, sells[0], sells[1])
            did_action = True
    for buys in info['book_buy']:
        if buys[0] > FV:
            if info['position'] > buys[1]:
                market.sell_order(stock, buys[0], buys[1])
                did_action = True
    return did_action

def penny(market, stock, info):
    if info['bid'] == 0:
        return
    penny_buy = info['bid']+1 
    penny_sell = info['ask']-1 
    temp = [values['price'] for values in market.get_orders(stock).values()]
    current_buy_order = max(temp) if len(temp) != 0 else 0
    if current_buy_order != info['bid']:
        market.buy_order(stock, penny_buy, 1)
    # Check if we have stock
    if 1 <= info['position']:
        market.sell_order(stock, penny_sell, 1)
        return
    else:
        return
   
def ETF_strategy(stocks):
    # Calculate the best buys and sells for a stock
    if stock == "CORGE":
        sell_profit = stocks["CORGE"]['ask']*10 - stocks["FOO"]['bid']*3 - stocks["BAR"]['bid']*8
        buy_profit = stocks["FOO"]['bid']*3 + stocks["BAR"]['bid']*8 - stocks["CORGE"]['ask']*10
    else:
        return -1

def order_timeout(orders):
    current_time = time.time()
    for order, order_info in orders:
        if current_time - order_info['timestamp'] > turnover:
            market.cancel_order(order)


# USE THIS FUNCTION:
def next_action(market):
    # takes in a market, computes a fair value, outputs some action based on strategy
    order_timeout(market.orders)
    
    for stock, info in market.stocks.items():
        if market.num_orders() < num_orders:
            did_action = FV_attempt(market, stock, info)
            if not did_action: penny(market, stock, info)
        
        
        
