import market

# Given a market state, output a fair value, 

def fair_value(stock):
    # Halfway point between best bid and best offer for stock
    best_bid = stock[1]
    best_offer = stock[2]
    return best_bid + .5*(best_offer-best_bid)
    
def penny(stock, info):
    penny_buy = info[1]+1
    penny_sell = info[2]-1
    if (penny_buy - penny_sell) > 0:
        market.send_order("BUY", stock, penny_buy, 1)
        market.send_order("SELL", stock, penny_stock, 1)
        return
    else:
        return
   
    
def ETF_strategy(stocks):
    # Calculate the best buys and sells for a stock
    if stock == "CORGE":
        sell_profit = stocks["CORGE"][2]*10 - stocks["FOO"][1]*3 - stocks["BAR"][1]*8
        buy_profit = stocks["FOO"][2]*3 + stocks["BAR"][2]*8 - stocks["CORGE"][1]*10
    else:
        return -1

# USE THIS FUNCTION:

def next_action(market):
    # takes in a market, computes a fair value, outputs some action based on strategy   
    for stock, info in market.stocks:
        penny(stock, info)
        
        
        
