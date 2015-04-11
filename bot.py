import naive
from market import *
import util
import naive
import time

m = Market()
i = 0
while True:
    if i % 100 == 0:
        naive.next_action(m)
    m.update()
