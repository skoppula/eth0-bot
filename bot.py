import naive
import market
import util
import naive

m = Market()

while True:
    naive.next_action(m)
    market.update()
    # Update Market
    # Send next order
