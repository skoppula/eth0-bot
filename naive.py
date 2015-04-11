import market

# Given a market state, output a fair value, 

def fair_value(stock):
    # Halfway point between best bid and best offer for stock
    best_bid = stock['bid']
    best_offer = stock['ask']
    return best_bid + .5*(best_offer-best_bid)
    
def penny(stock, info):
    penny_buy = info['bid']+1
    penny_sell = info['ask']-1
    if (penny_buy - penny_sell) > 0:
        market.send_order("BUY", stock, penny_buy, 1)
        market.send_order("SELL", stock, penny_stock, 1)
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

# USE THIS FUNCTION:

def next_action(market):
    # takes in a market, computes a fair value, outputs some action based on strategy   
    for stock, info in market.stocks.items():
        penny(stock, info)
        
        
        
