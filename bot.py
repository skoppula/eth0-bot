import naive
from market import *
import util
import naive

m = Market()
i=0
while i<1000:
    naive.next_action(m)
    m.update()
    i += 1
    # Update Market
    # Send next order
