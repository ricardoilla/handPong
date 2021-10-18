import threading
from Game.pong import *


threads = []


t1 = threading.Thread(target=run_game)
t2 = threading.Thread(target=run_tracking)

threads.append(t1)
threads.append(t2)

t2.start()
t1.start()