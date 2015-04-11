import naive
from market import *
import util
import naive

m = Market()
while True:
    naive.next_action(m)
    m.update()
