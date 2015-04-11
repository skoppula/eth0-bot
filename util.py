import socket
import sys
import json

TEAM_NAME='SEA'
BOT_BOX_IP='52.4.171.0'
PASS='EcAyY836zTdcFnAh'
EX_PUBLIC_IP='52.5.76.103' #looking at observer
EX_PRIVATE_IP='10.0.37.99' #connecting from bot box

MARKET_INDEX = 0 #0 for slow, 1 for real, 2 for empty
#JSON_PORT = 25000+index
#PLAIN_TEXT_PORT = 20000+index

def setup_connection():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.connect(EX_PRIVATE_IP, JSON_PORT)
        s.connect(('127.0.0.1', 8080))
        return s

    except:
        print 'COULD NOT CONNECT'
        return None

def send_json(sckt, msg):
    sckt.send(json.dumps(msg))

def listen_for_message(sckt):
    infile = sckt.makefile()
    while True:
        line = infile.readline()
        #json.loads(s.recv(1024))
        print json.loads(line)

s = setup_connection()
listen_for_message(s)

def hello(sckt):
    hello_msg = {"type": "hello", "team": "SEA"}
    
def sell(sckt, order_id, symbol_id, price, size):
    pass

#def buy(sckt, order_id, symbol_id, price, size):

